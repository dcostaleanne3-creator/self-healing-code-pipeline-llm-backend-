from agents.llm_client import ask_llm


def generate_hint(error_info):

    print("Learning Agent Activated")

    error_type = error_info["error_type"]
    message = error_info["message"]

    prompt = f"""
You are a programming tutor helping a beginner developer.

The developer made this error:

Error Type: {error_type}
Error Message: {message}

Give a small hint that helps them think and find the solution.
Do not give the complete fix.
Encourage them to solve it themselves.
"""

    hint = ask_llm(prompt)

    return {
        "hint": hint
    }