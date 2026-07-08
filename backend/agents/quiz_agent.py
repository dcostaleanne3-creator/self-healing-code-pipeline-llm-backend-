from agents.llm_client import ask_llm


def generate_quiz(error_info, explanation):

    print("Quiz Agent Activated")

    error_type = error_info["error_type"]
    message = error_info["message"]

    prompt = f"""
You are a programming tutor.

Create a small quiz for a beginner developer based on this error.

Error Type:
{error_type}

Error Message:
{message}

Explanation:
{explanation}

Create:
1. One multiple-choice question.
2. Three options (A, B, C).
3. Mention the correct answer.
4. Keep it simple.
"""

    quiz = ask_llm(prompt)

    return {
        "quiz": quiz
    }