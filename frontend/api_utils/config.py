import os
from dotenv import load_dotenv

load_dotenv()

# Your Railway backend URL
API_BASE_URL = os.getenv("API_BASE_URL", "https://smartmathtutor-production.up.railway.app")

# API Endpoints
ENDPOINTS = {
    "create_user": f"{API_BASE_URL}/create_user",
    "start_session": f"{API_BASE_URL}/start_session",
    "next_question": f"{API_BASE_URL}/next_question",
    "submit_answer": f"{API_BASE_URL}/submit_answer"
}