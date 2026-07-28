from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os


from utils.url import extract_video_id

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
# 5. Create Vector Store
# -----------------------------------

retriever = create_vector_store(transcript)


# -----------------------------------
# 6. Create LLM
# -----------------------------------

llm = ChatGroq(

    api_key=os.getenv("GROQ_API_KEY"),

    model="llama-3.3-70b-versatile"
)


# -----------------------------------
# 7. Create Chains
# -----------------------------------

chat_chain = create_chat_chain(llm)

summary_chain = create_summary_chain(llm)

overview_chain = create_overview_chain(llm)

timestamp_chain = create_timestamp_chain(llm)


# -----------------------------------
# 8. Chat Loop
# -----------------------------------

while True:

    query = input("\nUser: ")

    query_lower = query.lower()


    # -------------------------------
    # Video Overview Feature
    # -------------------------------

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

        continue


    # -------------------------------
    # Summary Feature
    # -------------------------------

    if "summary" in query_lower:

        result = summary_chain.invoke({

    "full_text": full_text,

    "query": query

})

        print("\nAI:", result)

        continue


    # -------------------------------
    # Timestamp Feature
    # -------------------------------

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

        continue


    # -------------------------------
    # Normal RAG Chat
    # -------------------------------

    results = retriever.invoke(query)


    context = ""


    for doc in results:

        context += f"""

        Timestamp: {doc.metadata['start']}

        Content:
        {doc.page_content}

        """


    result = chat_chain.invoke({

        "query": query,

        "context": context

    })


    print("\nAI:", result)