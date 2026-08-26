from fastapi import APIRouter, HTTPException

from api import state

from langchain_google_genai import (
    ChatGoogleGenerativeAI
)

from api.schemas.models import ChatRequest

from features.important_timestamps import (
    create_important_timestamps_chain
)

from features.translation import (
    create_translation_chain
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

from memory.conversation_memory import (
    get_memory
)

from dotenv import load_dotenv

import os


# ===================================
# ENVIRONMENT
# ===================================

load_dotenv()


# ===================================
# ROUTER
# ===================================

router = APIRouter(
    prefix="/api",
    tags=["Features"]
)


# ===================================
# LLM
# ===================================

llm = ChatGoogleGenerativeAI(

    google_api_key=os.getenv(
        "GEMINI_API_KEY"
    ),

    model="gemini-2.5-flash",

    temperature=0
)


# ===================================
# CHAINS
# ===================================

important_timestamps_chain = (
    create_important_timestamps_chain(llm)
)

translation_chain = (
    create_translation_chain(llm)
)

study_notes_chain = (
    create_study_notes_chain(llm)
)

quiz_chain = (
    create_quiz_chain(llm)
)

flashcards_chain = (
    create_flashcards_chain(llm)
)

chapters_chain = (
    create_chapters_chain(llm)
)


# ===================================
# HELPER
# ===================================

def require_video():

    if not state.video_transcripts:

        raise HTTPException(

            status_code=400,

            detail=(
                "No video has been added yet. "
                "Add a YouTube video first."
            )

        )


# ===================================
# IMPORTANT TIMESTAMPS
# ===================================

@router.post("/important-timestamps")
def important_timestamps():

    require_video()

    try:

        result = (
            important_timestamps_chain.invoke({

                "transcript":
                    "\n\n".join(
                        state.timestamped_sections
                    )

            })
        )

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=(
                "Important timestamps error: "
                f"{str(e)}"
            )

        )

    return {

        "response": result

    }


# ===================================
# TRANSLATION
# ===================================

@router.post("/translate")
def translate(
    request: ChatRequest
):

    query = request.query.strip()


    # -----------------------------------
    # Validate Query
    # -----------------------------------

    if not query:

        raise HTTPException(

            status_code=400,

            detail="Query cannot be empty."

        )


    # -----------------------------------
    # Get Memory
    # -----------------------------------

    memory = get_memory()


    if not memory:

        raise HTTPException(

            status_code=400,

            detail=(
                "There is no previous response "
                "to translate."
            )

        )


    # -----------------------------------
    # Extract Last AI Response
    # -----------------------------------

    lines = memory.splitlines()

    last_ai_response = None


    for i in range(
        len(lines) - 1,
        -1,
        -1
    ):

        if lines[i].startswith("AI:"):

            ai_lines = [

                lines[i]
                .replace(
                    "AI:",
                    "",
                    1
                )
                .strip()

            ]


            # Collect all lines belonging
            # to this AI response

            for j in range(
                i + 1,
                len(lines)
            ):

                # Stop when the next
                # USER message begins

                if lines[j].startswith(
                    "USER:"
                ):

                    break


                ai_lines.append(
                    lines[j]
                )


            last_ai_response = (
                "\n".join(ai_lines)
                .strip()
            )

            break


    # -----------------------------------
    # Validate AI Response
    # -----------------------------------

    if not last_ai_response:

        raise HTTPException(

            status_code=400,

            detail=(
                "No previous AI response "
                "was found."
            )

        )


    # -----------------------------------
    # Translation
    # -----------------------------------

    try:

        result = (
            translation_chain.invoke({

                "query": query,

                "text": last_ai_response

            })
        )

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=(
                "Translation error: "
                f"{str(e)}"
            )

        )


    # -----------------------------------
    # Return Translation
    # -----------------------------------

    return {

        "response": result

    }


# ===================================
# STUDY NOTES
# ===================================

@router.post("/study-notes")
def study_notes():

    require_video()

    try:

        result = (
            study_notes_chain.invoke({

                "transcript":
                    state.full_text

            })
        )

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=(
                "Study notes error: "
                f"{str(e)}"
            )

        )

    return {

        "response": result

    }


# ===================================
# QUIZ
# ===================================

@router.post("/quiz")
def quiz():

    require_video()

    try:

        result = (
            quiz_chain.invoke({

                "transcript":
                    state.full_text

            })
        )

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=(
                "Quiz error: "
                f"{str(e)}"
            )

        )

    return {

        "response": result

    }


# ===================================
# FLASHCARDS
# ===================================

@router.post("/flashcards")
def flashcards():

    require_video()

    try:

        result = (
            flashcards_chain.invoke({

                "transcript":
                    state.full_text

            })
        )

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=(
                "Flashcards error: "
                f"{str(e)}"
            )

        )

    return {

        "response": result

    }


# ===================================
# CHAPTERS
# ===================================

@router.post("/chapters")
def chapters():

    require_video()

    try:

        result = (
            chapters_chain.invoke({

                "full_text":
                    state.full_text,

                "transcript":
                    state.full_text

            })
        )

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=(
                "Chapters error: "
                f"{str(e)}"
            )

        )

    return {

        "response": result

    }