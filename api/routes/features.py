from fastapi import APIRouter, HTTPException

from api import state

from api.schemas.models import TranslationRequest

from features.summary import create_summary_chain
from features.overview import create_overview_chain
from features.important_timestamps import (
    create_important_timestamps_chain
)
from features.translation import create_translation_chain
from features.study_notes import create_study_notes_chain
from features.quiz import create_quiz_chain
from features.flashcards import create_flashcards_chain
from features.chapters import create_chapters_chain

from langchain_groq import ChatGroq

from dotenv import load_dotenv

import os


load_dotenv()


# ===================================
# ROUTER
# ===================================

router = APIRouter(
    prefix="/api",
    tags=["Features"]
)


# ===================================
# CREATE LLM
# ===================================

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile"
)


# ===================================
# CREATE FEATURE CHAINS
# ===================================

summary_chain = create_summary_chain(llm)

overview_chain = create_overview_chain(llm)

important_timestamps_chain = (
    create_important_timestamps_chain(llm)
)

translation_chain = create_translation_chain(llm)

study_notes_chain = create_study_notes_chain(llm)

quiz_chain = create_quiz_chain(llm)

flashcards_chain = create_flashcards_chain(llm)

chapters_chain = create_chapters_chain(llm)


# ===================================
# SUMMARY
# ===================================

@router.post("/summary")
def summary():

    if not state.full_text:

        raise HTTPException(
            status_code=400,
            detail=(
                "No video has been added yet. "
                "Add a YouTube video first."
            )
        )

    try:

        result = summary_chain.invoke({

            "full_text": state.full_text,

            "query": (
                "Give me a clear and useful "
                "summary of this video."
            )

        })

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Summary error: {str(e)}"
        )

    return {
        "response": result
    }


# ===================================
# OVERVIEW
# ===================================

@router.post("/overview")
def overview():

    if not state.full_text:

        raise HTTPException(
            status_code=400,
            detail=(
                "No video has been added yet. "
                "Add a YouTube video first."
            )
        )

    try:

        result = overview_chain.invoke({

            "full_text": state.full_text,

            "query": (
                "What is this video about? "
                "Explain the main topic and "
                "key ideas clearly."
            )

        })

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Overview error: {str(e)}"
        )

    return {
        "response": result
    }


# ===================================
# IMPORTANT TIMESTAMPS
# ===================================

@router.post("/important-timestamps")
def important_timestamps():

    if not state.timestamped_sections:

        raise HTTPException(
            status_code=400,
            detail=(
                "No video has been added yet. "
                "Add a YouTube video first."
            )
        )

    transcript = "\n\n".join(
        state.timestamped_sections
    )

    try:

        result = important_timestamps_chain.invoke({

            "transcript": transcript

        })

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
    request: TranslationRequest
):

    if not request.query.strip():

        raise HTTPException(
            status_code=400,
            detail="Query cannot be empty."
        )

    try:

        result = translation_chain.invoke({

            "query": request.query,

            "text": request.query

        })

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Translation error: {str(e)}"
        )

    return {
        "response": result
    }


# ===================================
# STUDY NOTES
# ===================================

@router.post("/study-notes")
def study_notes():

    if not state.full_text:

        raise HTTPException(
            status_code=400,
            detail=(
                "No video has been added yet. "
                "Add a YouTube video first."
            )
        )

    try:

        result = study_notes_chain.invoke({

            "transcript": state.full_text

        })

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Study notes error: {str(e)}"
        )

    return {
        "response": result
    }


# ===================================
# QUIZ
# ===================================

@router.post("/quiz")
def quiz():

    if not state.full_text:

        raise HTTPException(
            status_code=400,
            detail=(
                "No video has been added yet. "
                "Add a YouTube video first."
            )
        )

    try:

        result = quiz_chain.invoke({

            "transcript": state.full_text

        })

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Quiz error: {str(e)}"
        )

    return {
        "response": result
    }


# ===================================
# FLASHCARDS
# ===================================

@router.post("/flashcards")
def flashcards():

    if not state.full_text:

        raise HTTPException(
            status_code=400,
            detail=(
                "No video has been added yet. "
                "Add a YouTube video first."
            )
        )

    try:

        result = flashcards_chain.invoke({

            "full_text": state.full_text,

            "transcript": state.full_text

        })

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Flashcards error: {str(e)}"
        )

    return {
        "response": result
    }


# ===================================
# CHAPTERS
# ===================================

@router.post("/chapters")
def chapters():

    if not state.full_text:

        raise HTTPException(
            status_code=400,
            detail=(
                "No video has been added yet. "
                "Add a YouTube video first."
            )
        )

    try:

        result = chapters_chain.invoke({

            "full_text": state.full_text,

            "transcript": state.full_text

        })

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Chapters error: {str(e)}"
        )

    return {
        "response": result
    }