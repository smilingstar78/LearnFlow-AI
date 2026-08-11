from fastapi import APIRouter, HTTPException

from api.schemas.models import ChatRequest

from api import state

from features.chat import create_chat_chain
from features.overview import create_overview_chain

from memory.conversation_memory import (
    add_to_memory,
    get_memory
)

from langchain_groq import ChatGroq

from dotenv import load_dotenv

import os


load_dotenv()


router = APIRouter(
    prefix="/api",
    tags=["Chat"]
)


# ===================================
# CREATE LLM
# ===================================

llm = ChatGroq(

    api_key=os.getenv(
        "GROQ_API_KEY"
    ),

    model="llama-3.3-70b-versatile"

)


# ===================================
# CREATE CHAINS
# ===================================

chat_chain = create_chat_chain(
    llm
)

overview_chain = create_overview_chain(
    llm
)


# ===================================
# CHAT
# ===================================

@router.post("/chat")
def chat(request: ChatRequest):

    # -----------------------------------
    # Check Video
    # -----------------------------------

    if not state.video_transcripts:

        raise HTTPException(

            status_code=400,

            detail=(
                "No video has been added yet. "
                "Add a YouTube video first."
            )

        )


    query_lower = request.query.lower()


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

        try:

            result = overview_chain.invoke({

                "full_text": state.full_text,

                "query": request.query

            })


        except Exception as e:

            raise HTTPException(

                status_code=500,

                detail=f"Overview error: {str(e)}"

            )


        add_to_memory(

            request.query,

            result

        )


        return {

            "query": request.query,

            "response": result

        }


    # ===================================
    # NORMAL RAG CHAT
    # ===================================

    if state.retriever is None:

        raise HTTPException(

            status_code=400,

            detail="Retriever is not available."

        )


    # -----------------------------------
    # Retrieve Relevant Documents
    # -----------------------------------

    try:

        results = state.retriever.invoke(

            request.query

        )


    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=f"Retrieval error: {str(e)}"

        )


    # -----------------------------------
    # Build Context
    # -----------------------------------

    context = ""


    for doc in results:

        context += f"""

Video ID:
{doc.metadata.get(
    "video_id",
    "Unknown"
)}

Timestamp:
{doc.metadata.get(
    "start",
    "Unknown"
)}

Content:
{doc.page_content}

"""


    # -----------------------------------
    # Memory
    # -----------------------------------

    memory = get_memory()


    # -----------------------------------
    # Generate Answer
    # -----------------------------------

    try:

        result = chat_chain.invoke({

            "query": request.query,

            "context": context,

            "memory": memory

        })


    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=f"LLM error: {str(e)}"

        )


    # -----------------------------------
    # Save Memory
    # -----------------------------------

    add_to_memory(

        request.query,

        result

    )


    # -----------------------------------
    # Response
    # -----------------------------------

    return {

        "query": request.query,

        "response": result

    }