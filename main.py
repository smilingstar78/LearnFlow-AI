from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


# ===================================
# ROUTES
# ===================================

from api.routes.video import (
    router as video_router
)

from api.routes.chat import (
    router as chat_router
)

from api.routes.features import (
    router as features_router
)


# ===================================
# CREATE APP
# ===================================

app = FastAPI(

    title="LearnFlow AI",

    description=(
        "AI-powered YouTube learning "
        "assistant with RAG, summaries, "
        "quizzes, flashcards, study notes "
        "and more."
    ),

    version="1.0.0"

)


# ===================================
# CORS
# ===================================

app.add_middleware(

    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]

)


# ===================================
# INCLUDE ROUTERS
# ===================================

app.include_router(
    video_router
)

app.include_router(
    chat_router
)

app.include_router(
    features_router
)


# ===================================
# ROOT
# ===================================

@app.get("/")
def home():

    return {

        "message":
            "Welcome to LearnFlow AI API 🚀"

    }


# ===================================
# HEALTH CHECK
# ===================================

@app.get("/health")
def health_check():

    return {

        "status": "healthy",

        "service": "LearnFlow AI"

    }