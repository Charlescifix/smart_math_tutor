import random

def generate_math_question(difficulty: int = 1) -> dict:
    """
    Generate a math question based on difficulty level (1-5).
    Returns question_text, correct_answer, difficulty
    """
    if difficulty < 1:
        difficulty = 1
    if difficulty > 5:
        difficulty = 5

    question_type = random.choice(["add", "sub", "mul", "div"]) if difficulty >= 2 else "add"

    if difficulty == 1:
        a, b = random.randint(1, 9), random.randint(1, 9)
    elif difficulty == 2:
        a, b = random.randint(10, 30), random.randint(5, 15)
    elif difficulty == 3:
        a, b = random.randint(20, 50), random.randint(10, 25)
    elif difficulty == 4:
        a, b = random.randint(50, 100), random.randint(10, 50)
    else:  # Level 5
        a, b = random.randint(100, 999), random.randint(10, 99)

    if question_type == "add":
        question_text = f"What is {a} + {b}?"
        correct_answer = str(a + b)
    elif question_type == "sub":
        question_text = f"What is {a} - {b}?"
        correct_answer = str(a - b)
    elif question_type == "mul":
        question_text = f"What is {a} × {b}?"
        correct_answer = str(a * b)
    elif question_type == "div":
        # Ensure divisible
        result = a * b
        question_text = f"What is {result} ÷ {b}?"
        correct_answer = str(result // b)
    else:
        question_text = "What is 1 + 1?"
        correct_answer = "2"

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "difficulty": difficulty
    }
