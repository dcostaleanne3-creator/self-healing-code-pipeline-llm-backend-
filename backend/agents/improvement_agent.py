from agents.llm_client import ask_llm


def suggest_improvements(code, fixed_code):

    print("Improvement Agent Activated")

    prompt = f"""
You are a Python code quality expert.

Analyze the original code and the fixed code below.

Original Code:
{code}

Fixed Code:
{fixed_code}

Suggest improvements that can make the code:
- cleaner
- more readable
- more efficient
- easier for beginners to understand

Give short bullet point suggestions.
"""

    suggestions = ask_llm(prompt)

    return {
        "suggestions": suggestions
    }