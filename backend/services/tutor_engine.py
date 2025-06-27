from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import os
from dotenv import load_dotenv

# Ensure environment is loaded
load_dotenv()

# Get API key safely
api_key = os.getenv("OPENAI_API_KEY")

# ✅ Pass it directly into the model
llm = ChatOpenAI(
    model="gpt-4",         # or "gpt-4-turbo"
    temperature=0.5,
    api_key=api_key        # <== This line is crucial
)


def get_feedback(question_text: str, correct_answer: str, student_answer: str, difficulty: int) -> dict:
    """
    Returns intelligent feedback and adjusted difficulty based on student's answer.
    """
    system_prompt = (
        "You are a friendly and encouraging math tutor for creative children aged 8–12. "
        "Always explain in a clear and simple way, using relatable examples. "
        "If the student makes a mistake, gently explain what went wrong and guide them toward the correct concept. "
        "If they get it right, praise them and increase the difficulty a little."
    )

    user_prompt = (
        f"Question: {question_text}\n"
        f"Correct Answer: {correct_answer}\n"
        f"Student Answer: {student_answer}\n\n"
        f"Was the student correct? Give a short explanation. Then suggest the next difficulty level "
        f"(1-5, where 5 is hardest) as 'next_difficulty'.\n\n"
        f"Respond in this format:\n"
        f"[FEEDBACK]: <your feedback here>\n"
        f"[NEXT_DIFFICULTY]: <level>"
    )

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ]

    response = llm.invoke(messages)

    # Basic parsing
    feedback_lines = response.content.split("\n")
    feedback = ""
    next_level = difficulty  # default if parse fails

    for line in feedback_lines:
        if line.startswith("[FEEDBACK]:"):
            feedback = line.replace("[FEEDBACK]:", "").strip()
        elif line.startswith("[NEXT_DIFFICULTY]:"):
            try:
                next_level = int(line.replace("[NEXT_DIFFICULTY]:", "").strip())
            except:
                pass

    return {
        "feedback": feedback,
        "next_difficulty": next_level
    }
