from fastapi import FastAPI


# ===================================
# ROUTES
# ===================================

from api.routes.video import router as video_router

from api.routes.chat import router as chat_router

from api.routes.features import (
    router as features_router
)


# ===================================
# CREATE FASTAPI APP
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

        "message": (
            "Welcome to LearnFlow AI API 🚀"
        )

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