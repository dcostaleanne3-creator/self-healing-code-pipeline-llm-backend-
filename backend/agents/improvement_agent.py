from agents.llm_client import ask_llm


def suggest_improvements(code, fixed_code=None):

    print("Improvement Agent Activated")

    if fixed_code:
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
    else:
        prompt = f"""
You are a Python code quality expert reviewing a beginner developer's code.

Code:
{code}

Point out specific parts of this code that could be written better, and suggest
how to improve them (readability, efficiency, naming, structure, best practices).

Give short bullet point suggestions, referencing the specific line or part of code
where relevant.
"""

    suggestions = ask_llm(prompt)

    return {
        "suggestions": suggestions
    }