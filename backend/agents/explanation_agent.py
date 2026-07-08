from agents.llm_client import ask_llm

def explain_error(error_info):

    print("Explanation Agent Activated")

    error_type = error_info["error_type"]
    message = error_info["message"]

    prompt = f"""
Explain this Python error to a beginner developer.

Error Type: {error_type}
Message: {message}

Keep the explanation simple.
"""

    explanation = ask_llm(prompt)

    return {
        "explanation": explanation
    }