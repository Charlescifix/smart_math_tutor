from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db import models
from backend.db.database import SessionLocal
from backend.schemas import schema
from backend.services.tutor_engine import get_feedback
from backend.services.rewards import update_points_and_streak, assign_badge
from backend.services.math_engine import generate_math_question

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.post("/create_user")
def create_user(payload: schema.UserCreate, db: Session = Depends(get_db)):
    user = models.User(
        name=payload.name,
        age=payload.age,
        grade_level=payload.grade_level
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"user_id": user.id}



@router.post("/start_session")
def start_session(payload: schema.SessionCreate, db: Session = Depends(get_db)):
    # Check if user exists (optional)
    user = db.query(models.User).filter_by(id=payload.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    session = models.Session(
        user_id=payload.user_id
    )
    db.add(session)
    db.commit()
    db.refresh(session)

    return {"session_id": session.id}

@router.post("/submit_answer")
def submit_answer(payload: schema.AnswerSubmission, db: Session = Depends(get_db)):
    # 1. Get the session
    session = db.query(models.Session).filter_by(id=payload.session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")

    # 2. Get the latest unanswered question
    question = (
        db.query(models.Question)
        .filter_by(session_id=payload.session_id)
        .order_by(models.Question.id.desc())
        .first()
    )
    if not question:
        raise HTTPException(status_code=404, detail="Question not found.")

    # 3. Validate answer
    was_correct = payload.student_answer.strip() == question.correct_answer.strip()
    question.student_answer = payload.student_answer
    question.was_correct = was_correct

    # 4. Generate feedback using LLM
    tutor_response = get_feedback(
        question_text=question.question_text,
        correct_answer=question.correct_answer,
        student_answer=payload.student_answer,
        difficulty=question.difficulty
    )
    question.feedback = tutor_response["feedback"]

    # 5. Update session score, streak, level
    update_points_and_streak(session, was_correct)
    badge = assign_badge(session.streak, session.level)

    # 6. Save updates
    db.commit()

    return {
        "feedback": tutor_response["feedback"],
        "next_difficulty": tutor_response["next_difficulty"],
        "was_correct": was_correct,
        "score": session.score,
        "streak": session.streak,
        "max_streak": session.max_streak,
        "level": session.level,
        "badge": badge
    }

@router.get("/next_question/{session_id}")
def get_next_question(session_id: int, db: Session = Depends(get_db)):
    session = db.query(models.Session).filter_by(id=session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")

    # Generate a question using current session level
    new_q = generate_math_question(session.level)

    # Save the question in DB
    question = models.Question(
        session_id=session_id,
        question_text=new_q["question_text"],
        correct_answer=new_q["correct_answer"],
        difficulty=new_q["difficulty"]
    )
    db.add(question)
    db.commit()
    db.refresh(question)

    return {
        "question_id": question.id,
        "question_text": question.question_text,
        "difficulty": question.difficulty
    }
