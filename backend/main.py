from fastapi import FastAPI
from backend.api.routes import router

app = FastAPI(
    title="Smart Math Tutor",
    description="An AI-powered math learning assistant for kids",
    version="1.0.0"
)

app.include_router(router)
