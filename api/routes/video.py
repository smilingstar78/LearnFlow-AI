from fastapi import APIRouter, HTTPException

from api.schemas.models import VideoRequest

from api import state

from utils.url import extract_video_id

from services.transcript_service import fetch_transcript

from services.vector_store import create_vector_store


router = APIRouter(
    prefix="/api/videos",
    tags=["Videos"]
)


# ===================================
# ADD VIDEO
# ===================================

@router.post("/")
def add_video(request: VideoRequest):

    # -----------------------------------
    # Extract Video ID
    # -----------------------------------

    video_id = extract_video_id(
        request.url
    )


    if video_id is None:

        raise HTTPException(
            status_code=400,
            detail="Invalid YouTube URL"
        )


    # -----------------------------------
    # Fetch Transcript
    # -----------------------------------

    try:

        transcript = fetch_transcript(
            video_id
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Transcript error: {str(e)}"
        )


    # -----------------------------------
    # Add Video To Session
    # -----------------------------------

    state.video_transcripts.append({

        "video_id": video_id,

        "transcript": transcript

    })


    # -----------------------------------
    # Create Full Text
    # -----------------------------------

    state.full_text = ""


    for video in state.video_transcripts:

        state.full_text += "\n\n"


        state.full_text += "\n".join(

            snippet.text

            for snippet in video["transcript"]

        )


    # -----------------------------------
    # Create Timestamped Transcript
    # -----------------------------------

    state.timestamped_sections = []


    current_section = ""


    for video in state.video_transcripts:

        current_video_id = video["video_id"]


        for snippet in video["transcript"]:

            current_section += f"""

Video ID: {current_video_id}

Timestamp: {snippet.start}

Content:
{snippet.text}

"""


            if len(current_section) >= 12000:

                state.timestamped_sections.append(
                    current_section
                )

                current_section = ""


    if current_section:

        state.timestamped_sections.append(
            current_section
        )


    # -----------------------------------
    # Create / Rebuild Vector Store
    # -----------------------------------

    try:

        state.retriever = create_vector_store(
            state.video_transcripts
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Vector store error: {str(e)}"
        )


    # -----------------------------------
    # Response
    # -----------------------------------

    return {

        "message": "Video added successfully",

        "video_id": video_id,

        "total_videos": len(
            state.video_transcripts
        ),

        "transcript_chunks": len(
            transcript
        )

    }