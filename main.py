from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

from features.important_timestamps import (
    create_important_timestamps_chain
)

from memory.conversation_memory import (
    add_to_memory,
    get_memory
)

from utils.url import extract_video_id

from features.translation import create_translation_chain

from services.transcript_service import fetch_transcript

from services.vector_store import create_vector_store

from features.chat import create_chat_chain

from features.summary import create_summary_chain

from features.overview import create_overview_chain

from features.timestamp import (
    extract_timestamp,
    get_timestamp_context,
    create_timestamp_chain
)


load_dotenv()


# -----------------------------------
# 1. Get YouTube URL
# -----------------------------------

url = input("Paste URL: ")


# -----------------------------------
# 2. Extract Video ID
# -----------------------------------

video_id = extract_video_id(url)


# -----------------------------------
# 3. Fetch Transcript
# -----------------------------------

transcript = fetch_transcript(video_id)


# -----------------------------------
# 4. Create Full Text
# -----------------------------------

full_text = " ".join(
    snippet.text
    for snippet in transcript
)


# -----------------------------------
# 5. Create Timestamped Transcript
# -----------------------------------

timestamped_sections = []

current_section = ""

for snippet in transcript:

    current_section += f"""
Timestamp: {snippet.start}

Content:
{snippet.text}
"""

    # Keep each section reasonably small
    if len(current_section) >= 12000:

        timestamped_sections.append(current_section)

        current_section = ""


# Add remaining transcript
if current_section:

    timestamped_sections.append(current_section)


print(
    f"Transcript divided into "
    f"{len(timestamped_sections)} sections."
)


# -----------------------------------
# 6. Create Vector Store
# -----------------------------------

retriever = create_vector_store(transcript)


# -----------------------------------
# 7. Create LLM
# -----------------------------------

llm = ChatGroq(

    api_key=os.getenv("GROQ_API_KEY"),

    model="llama-3.3-70b-versatile"

)


# -----------------------------------
# 8. Create Chains
# -----------------------------------

chat_chain = create_chat_chain(llm)

summary_chain = create_summary_chain(llm)

overview_chain = create_overview_chain(llm)

timestamp_chain = create_timestamp_chain(llm)

translation_chain = create_translation_chain(llm)

important_timestamps_chain = (
    create_important_timestamps_chain(llm)
)


# -----------------------------------
# 9. Conversation Memory
# -----------------------------------

last_ai_response = ""


# -----------------------------------
# 10. Chat Loop
# -----------------------------------

while True:

    query = input("\nUser: ")

    query_lower = query.lower()


    # ===================================
    # IMPORTANT TIMESTAMPS
    # ===================================

    if (
        "important timestamps" in query_lower
        or "important moments" in query_lower
        or "key timestamps" in query_lower
        or "key moments" in query_lower
    ):

        all_results = []


        for section in timestamped_sections:

            result = important_timestamps_chain.invoke({

                "transcript": section

            })

            all_results.append(result)


        final_result = "\n\n".join(
            all_results
        )


        print("\nAI:", final_result)


        last_ai_response = final_result


        add_to_memory(

            query,

            final_result

        )


        continue


    # ===================================
    # TRANSLATION
    # ===================================

    translation_keywords = [

        "translate",

        "translation",

        "translate this",

        "translate it",

        "in urdu",

        "in english",

        "in hindi",

        "in french",

        "in arabic",

        "in turkish"

    ]


    if any(
        word in query_lower
        for word in translation_keywords
    ):

        if last_ai_response == "":

            print(
                "\nAI: There is nothing "
                "to translate yet."
            )

            continue


        result = translation_chain.invoke({

            "query": query,

            "text": last_ai_response

        })


        print("\nAI:", result)


        last_ai_response = result


        add_to_memory(

            query,

            result

        )


        continue


    # ===================================
    # VIDEO OVERVIEW
    # ===================================

    if (
        "what is this video about" in query_lower
        or "what is the video about" in query_lower
        or "tell me about this video" in query_lower
    ):

        result = overview_chain.invoke({

            "full_text": full_text,

            "query": query

        })


        print("\nAI:", result)


        last_ai_response = result


        add_to_memory(

            query,

            result

        )


        continue


    # ===================================
    # SUMMARY
    # ===================================

    if (
        "summary" in query_lower
        or "summarize" in query_lower
        or "summarise" in query_lower
    ):

        result = summary_chain.invoke({

            "full_text": full_text,

            "query": query

        })


        print("\nAI:", result)


        last_ai_response = result


        add_to_memory(

            query,

            result

        )


        continue


    # ===================================
    # SPECIFIC TIMESTAMP
    # ===================================

    timestamp = extract_timestamp(query)


    if timestamp is not None:

        timestamp_context = get_timestamp_context(

            transcript,

            timestamp

        )


        result = timestamp_chain.invoke({

            "context": timestamp_context,

            "query": query

        })


        print("\nAI:", result)


        last_ai_response = result


        add_to_memory(

            query,

            result

        )


        continue


    # ===================================
    # NORMAL RAG CHAT
    # ===================================

    results = retriever.invoke(query)


    context = ""


    for doc in results:

        context += f"""

Timestamp: {doc.metadata['start']}

Content:
{doc.page_content}

"""


    # Get previous conversation
    memory = get_memory()


    result = chat_chain.invoke({

        "query": query,

        "context": context,

        "memory": memory

    })


    print("\nAI:", result)


    last_ai_response = result


    add_to_memory(

        query,

        result

    )