from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from backend.db.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)
    grade_level = Column(String)
    sessions = relationship("Session", back_populates="user")

from sqlalchemy import Integer, Column, Float

class Session(Base):
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime, nullable=True)

    score = Column(Float, default=0.0)            # ✅ Total points
    streak = Column(Integer, default=0)            # ✅ Current streak
    max_streak = Column(Integer, default=0)        # ✅ Highest streak reached
    level = Column(Integer, default=1)

    user = relationship("User", back_populates="sessions")
    questions = relationship("Question", back_populates="session")



class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"))
    question_text = Column(String)
    correct_answer = Column(String)
    student_answer = Column(String)
    was_correct = Column(Boolean)
    difficulty = Column(Integer)
    feedback = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    session = relationship("Session", back_populates="questions")
