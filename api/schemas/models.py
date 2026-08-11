from pydantic import BaseModel


# ===================================
# ADD VIDEO REQUEST
# ===================================

class VideoRequest(BaseModel):

    url: str


# ===================================
# CHAT REQUEST
# ===================================

class ChatRequest(BaseModel):

    query: str


# ===================================
# TRANSLATION REQUEST
# ===================================

class TranslationRequest(BaseModel):

    query: str