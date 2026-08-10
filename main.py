from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os


# -----------------------------------
# Feature Imports
# -----------------------------------

from features.chat import create_chat_chain

from features.summary import create_summary_chain

from features.overview import create_overview_chain

from features.translation import create_translation_chain

from features.important_timestamps import (
    create_important_timestamps_chain
)

from features.study_notes import (
    create_study_notes_chain
)

from features.quiz import (
    create_quiz_chain
)

from features.flashcards import (
    create_flashcards_chain
)

from features.chapters import (
    create_chapters_chain
)

from features.timestamp import (
    extract_timestamp,
    get_timestamp_context,
    create_timestamp_chain
)


# -----------------------------------
# Memory
# -----------------------------------

from memory.conversation_memory import (
    add_to_memory,
    get_memory
)


# -----------------------------------
# Services / Utils
# -----------------------------------

from utils.url import extract_video_id

from services.transcript_service import (
    fetch_transcript
)

from services.vector_store import (
    create_vector_store
)


load_dotenv()


# ===================================
# 1. GET FIRST YOUTUBE VIDEO
# ===================================

video_transcripts = []


url = input("Paste YouTube URL: ")


video_id = extract_video_id(url)


if video_id is None:

    print("Invalid YouTube URL.")

    exit()


print("Fetching transcript...")


transcript = fetch_transcript(video_id)


video_transcripts.append({

    "video_id": video_id,

    "transcript": transcript

})


print("Video added successfully!")


# ===================================
# 2. OPTIONAL MULTIPLE VIDEOS
# ===================================

while True:

    add_more = input(
        "\nDo you want to add another video? (y/n): "
    ).lower()


    if add_more == "n":

        break


    elif add_more == "y":

        url = input(
            "Paste YouTube URL: "
        )


        video_id = extract_video_id(url)


        if video_id is None:

            print(
                "Invalid YouTube URL. Try again."
            )

            continue


        print(
            "Fetching transcript..."
        )


        transcript = fetch_transcript(
            video_id
        )


        video_transcripts.append({

            "video_id": video_id,

            "transcript": transcript

        })


        print(
            "Video added successfully!"
        )


    else:

        print(
            "Please enter y or n."
        )


print(
    f"\nTotal videos loaded: "
    f"{len(video_transcripts)}"
)


# ===================================
# 3. CREATE FULL TEXT
# ===================================

full_text = ""


for video in video_transcripts:

    full_text += "\n\n"


    full_text += "\n".join(

        snippet.text

        for snippet in video["transcript"]

    )


# ===================================
# 4. CREATE TIMESTAMPED SECTIONS
# ===================================

timestamped_sections = []


current_section = ""


for video in video_transcripts:

    video_id = video["video_id"]


    for snippet in video["transcript"]:

        current_section += f"""

Video ID: {video_id}

Timestamp: {snippet.start}

Content:
{snippet.text}

"""


        # Keep sections reasonably small
        # to avoid huge LLM requests

        if len(current_section) >= 12000:

            timestamped_sections.append(
                current_section
            )

            current_section = ""


# Add remaining content

if current_section:

    timestamped_sections.append(
        current_section
    )


print(
    f"Total transcript sections: "
    f"{len(timestamped_sections)}"
)


# ===================================
# 5. CREATE VECTOR STORE
# ===================================

retriever = create_vector_store(
    video_transcripts
)


# ===================================
# 6. CREATE LLM
# ===================================

llm = ChatGroq(

    api_key=os.getenv(
        "GROQ_API_KEY"
    ),

    model="llama-3.3-70b-versatile"
)


# ===================================
# 7. CREATE CHAINS
# ===================================

chat_chain = create_chat_chain(
    llm
)


summary_chain = create_summary_chain(
    llm
)


overview_chain = create_overview_chain(
    llm
)


timestamp_chain = create_timestamp_chain(
    llm
)


translation_chain = create_translation_chain(
    llm
)


important_timestamps_chain = (
    create_important_timestamps_chain(
        llm
    )
)


study_notes_chain = (
    create_study_notes_chain(
        llm
    )
)


quiz_chain = create_quiz_chain(
    llm
)


flashcards_chain = (
    create_flashcards_chain(
        llm
    )
)


chapters_chain = create_chapters_chain(
    llm
)


# ===================================
# 8. MEMORY
# ===================================

last_ai_response = ""


# ===================================
# 9. CHAT LOOP
# ===================================

while True:

    query = input("\nUser: ")


    query_lower = query.lower()


    # ===================================
    # EXIT
    # ===================================

    if query_lower in [
        "exit",
        "quit",
        "bye"
    ]:

        print(
            "\nAI: Goodbye! 👋"
        )

        break


    # ===================================
    # IMPORTANT TIMESTAMPS
    # ===================================

    if (
        "important timestamps"
        in query_lower

        or "important moments"
        in query_lower

        or "key timestamps"
        in query_lower

        or "key moments"
        in query_lower
    ):

        all_results = []


        for section in timestamped_sections:

            result = (
                important_timestamps_chain.invoke({

                    "transcript": section

                })
            )


            all_results.append(result)


        final_result = "\n\n".join(
            all_results
        )


        print(
            "\nAI:",
            final_result
        )


        last_ai_response = final_result


        add_to_memory(
            query,
            final_result
        )


        continue


    # ===================================
    # FLASHCARDS
    # ===================================

    if (
        "flashcards"
        in query_lower

        or "flash cards"
        in query_lower

        or "flashcard"
        in query_lower

        or "make flashcards"
        in query_lower

        or "generate flashcards"
        in query_lower
    ):

        all_flashcards = []


        for section in timestamped_sections:

            result = (
                flashcards_chain.invoke({

                    "transcript": section

                })
            )


            all_flashcards.append(result)


        final_flashcards = "\n\n".join(
            all_flashcards
        )


        print(
            "\nAI:",
            final_flashcards
        )


        last_ai_response = (
            final_flashcards
        )


        add_to_memory(
            query,
            final_flashcards
        )


        continue


    # ===================================
    # QUIZ GENERATOR
    # ===================================

    if (
        "quiz"
        in query_lower

        or "mcq"
        in query_lower

        or "mcqs"
        in query_lower

        or "test me"
        in query_lower

        or "create questions"
        in query_lower
    ):

        all_quizzes = []


        for section in timestamped_sections:

            result = (
                quiz_chain.invoke({

                    "transcript": section

                })
            )


            all_quizzes.append(result)


        final_quiz = "\n\n".join(
            all_quizzes
        )


        print(
            "\nAI:",
            final_quiz
        )


        last_ai_response = final_quiz


        add_to_memory(
            query,
            final_quiz
        )


        continue


    # ===================================
    # STUDY NOTES
    # ===================================

    if (
        "study notes"
        in query_lower

        or "study note"
        in query_lower

        or "make notes"
        in query_lower

        or "create notes"
        in query_lower

        or "generate notes"
        in query_lower
    ):

        all_notes = []


        for section in timestamped_sections:

            result = (
                study_notes_chain.invoke({

                    "transcript": section

                })
            )


            all_notes.append(result)


        final_notes = "\n\n".join(
            all_notes
        )


        print(
            "\nAI:",
            final_notes
        )


        last_ai_response = final_notes


        add_to_memory(
            query,
            final_notes
        )


        continue


    # ===================================
    # CHAPTER GENERATOR
    # ===================================

    if (
        "generate chapters"
        in query_lower

        or "create chapters"
        in query_lower

        or "video chapters"
        in query_lower

        or "make chapters"
        in query_lower

        or query_lower == "chapters"
    ):

        all_chapters = []


        for section in timestamped_sections:

            result = (
                chapters_chain.invoke({

                    "transcript": section

                })
            )


            all_chapters.append(result)


        final_chapters = "\n\n".join(
            all_chapters
        )


        print(
            "\nAI:",
            final_chapters
        )


        last_ai_response = (
            final_chapters
        )


        add_to_memory(
            query,
            final_chapters
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


        print(
            "\nAI:",
            result
        )


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
        "what is this video about"
        in query_lower

        or "what is the video about"
        in query_lower

        or "tell me about this video"
        in query_lower
    ):

        result = overview_chain.invoke({

            "full_text": full_text,

            "query": query

        })


        print(
            "\nAI:",
            result
        )


        last_ai_response = result


        add_to_memory(
            query,
            result
        )


        continue


    # ===================================
    # SUMMARY
    # ===================================

    if "summary" in query_lower:

        result = summary_chain.invoke({

            "full_text": full_text,

            "query": query

        })


        print(
            "\nAI:",
            result
        )


        last_ai_response = result


        add_to_memory(
            query,
            result
        )


        continue


    # ===================================
    # TIMESTAMP QUESTION
    # ===================================

    timestamp = extract_timestamp(
        query
    )


    if timestamp is not None:

        timestamp_context = (
            get_timestamp_context(

                # Use the first transcript
                # for the current timestamp
                # feature

                video_transcripts[0][
                    "transcript"
                ],

                timestamp

            )
        )


        result = timestamp_chain.invoke({

            "context": timestamp_context,

            "query": query

        })


        print(
            "\nAI:",
            result
        )


        last_ai_response = result


        add_to_memory(
            query,
            result
        )


        continue


    # ===================================
    # NORMAL RAG CHAT
    # ===================================

    results = retriever.invoke(
        query
    )


    context = ""


    for doc in results:

        context += f"""

Video ID:
{doc.metadata.get("video_id", "Unknown")}

Timestamp:
{doc.metadata.get("start", "Unknown")}

Content:
{doc.page_content}

"""


    # ===================================
    # GET MEMORY
    # ===================================

    memory = get_memory()


    # ===================================
    # ASK LLM
    # ===================================

    result = chat_chain.invoke({

        "query": query,

        "context": context,

        "memory": memory

    })


    print(
        "\nAI:",
        result
    )


    # ===================================
    # SAVE MEMORY
    # ===================================

    last_ai_response = result


    add_to_memory(
        query,
        result
    )