from pydantic import BaseModel


# ===================================
# VIDEO REQUEST
# ===================================

class VideoRequest(BaseModel):

    url: str


# ===================================
# CHAT REQUEST
# ===================================

class ChatRequest(BaseModel):

    query: str