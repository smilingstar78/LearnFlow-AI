from fastapi import APIRouter, HTTPException

from api import state

from api.schemas.models import ChatRequest

from features.chat import create_chat_chain

from features.timestamp import (
    extract_timestamp,
    get_timestamp_context,
    create_timestamp_chain
)

from features.overview import (
    create_overview_chain
)

from features.summary import (
    create_summary_chain
)

from memory.conversation_memory import (
    get_memory,
    add_to_memory
)

from langchain_groq import ChatGroq

from dotenv import load_dotenv

import os


# ===================================
# LOAD ENVIRONMENT
# ===================================

load_dotenv()


# ===================================
# ROUTER
# ===================================

router = APIRouter(
    prefix="/api",
    tags=["Chat"]
)


# ===================================
# LLM
# ===================================

llm = ChatGroq(

    api_key=os.getenv(
        "GROQ_API_KEY"
    ),

    model="llama-3.3-70b-versatile"

)


# ===================================
# CHAINS
# ===================================

chat_chain = create_chat_chain(
    llm
)

timestamp_chain = create_timestamp_chain(
    llm
)

overview_chain = create_overview_chain(
    llm
)

summary_chain = create_summary_chain(
    llm
)


# ===================================
# CHAT
# ===================================

@router.post("/chat")
def chat(request: ChatRequest):

    query = request.query.strip()


    # -----------------------------------
    # Empty Query
    # -----------------------------------

    if not query:

        raise HTTPException(
            status_code=400,
            detail="Query cannot be empty."
        )


    # -----------------------------------
    # Video Required
    # -----------------------------------

    if not state.video_transcripts:

        raise HTTPException(
            status_code=400,
            detail=(
                "No video has been added yet. "
                "Add a YouTube video first."
            )
        )


    query_lower = query.lower()


    # ===================================
    # TIMESTAMP QUESTION
    # ===================================

    timestamp = extract_timestamp(
        query
    )


    if timestamp is not None:

        try:

            # -----------------------------------
            # Use the first video's transcript
            # -----------------------------------

            transcript = (
                state.video_transcripts[0]["transcript"]
            )


            context = get_timestamp_context(

                transcript,

                timestamp

            )


            result = timestamp_chain.invoke({

                "context": context,

                "query": query

            })


        except Exception as e:

            raise HTTPException(
                status_code=500,
                detail=f"Timestamp error: {str(e)}"
            )


        add_to_memory(
            query,
            result
        )


        return {

            "response": result

        }


    # ===================================
    # OVERVIEW
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

                "query": query

            })


        except Exception as e:

            raise HTTPException(
                status_code=500,
                detail=f"Overview error: {str(e)}"
            )


        add_to_memory(
            query,
            result
        )


        return {

            "response": result

        }


    # ===================================
    # SUMMARY
    # ===================================

    if "summary" in query_lower:

        try:

            result = summary_chain.invoke({

                "full_text": state.full_text,

                "query": query

            })


        except Exception as e:

            raise HTTPException(
                status_code=500,
                detail=f"Summary error: {str(e)}"
            )


        add_to_memory(
            query,
            result
        )


        return {

            "response": result

        }


    # ===================================
    # NORMAL RAG
    # ===================================

    if state.retriever is None:

        raise HTTPException(
            status_code=500,
            detail="Retriever is not available."
        )


    # -----------------------------------
    # Retrieve Documents
    # -----------------------------------

    try:

        docs = state.retriever.invoke(
            query
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


    for doc in docs:

        context += f"""

Video ID:
{doc.metadata.get("video_id", "Unknown")}

Timestamp:
{doc.metadata.get("start", "Unknown")}

Content:
{doc.page_content}

"""


    # -----------------------------------
    # Conversation Memory
    # -----------------------------------

    memory = get_memory()


    # -----------------------------------
    # Chat Chain
    # -----------------------------------

    try:

        result = chat_chain.invoke({

            "query": query,

            "context": context,

            "memory": memory

        })


    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Chat error: {str(e)}"
        )


    # -----------------------------------
    # Save Conversation
    # -----------------------------------

    add_to_memory(
        query,
        result
    )


    # -----------------------------------
    # Response
    # -----------------------------------

    return {

        "response": result

    }