from agents.llm_client import ask_llm
from memory import get_error_count


def generate_hint(error_info, attempts):

    print("Learning Agent Activated")

    error_type = error_info["error_type"]
    message = error_info["message"]
    
    previous_count = get_error_count(
    error_info["error_type"]
)
    prompt = f"""
You are a coding tutor.

Error:
{error_info}

Give only a short hint to help the student fix the error.

Rules:
- Maximum 20 words
- Do not provide corrected code
- Do not explain theory

Attempt number: {attempts}

Hint strategy:
- Attempt 1: Give a general clue.
- Attempt 2: Give a more specific clue.
- Attempt 3: Give a very specific clue but do not give the solution.
"""

    hint = ask_llm(prompt)

    return {
        "hint": hint
    }