from agents.llm_client import ask_llm


def repair_code(code, error_info):

    print("Repair Agent Activated")

    error_type = error_info["error_type"]
    message = error_info["message"]

    prompt = f"""
You are a Python debugging expert.

Fix the following code.

Original Code:
{code}

Error Type:
{error_type}

Error Message:
{message}

Provide only the corrected Python code.
Do not explain.
"""

    fixed_code = ask_llm(prompt)

    return {
        "fixed_code": fixed_code
    }