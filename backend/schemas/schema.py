from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    age: int
    grade_level: str



class SessionCreate(BaseModel):
    user_id: int

class AnswerSubmission(BaseModel):
    session_id: int
    student_answer: str

class QuestionResponse(BaseModel):
    question_text: str
    difficulty: int
    question_id: int
