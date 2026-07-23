from agents.llm_client import ask_llm

def explain_error(error_info):

    print("Explanation Agent Activated")

    error_type = error_info["error_type"]
    message = error_info["message"]

    prompt = f"""
Explain this Python error to a beginner developer.

Error Type: {error_type}
Message: {message}

Break your explanation into 3-4 short steps.
Format EXACTLY like this, each step on its own line, starting with "STEP:":

STEP: <first short point>
STEP: <second short point>
STEP: <third short point>

Keep each step under 20 words. Do not include any other text.
"""

    raw = ask_llm(prompt)

    steps = [
        line.replace("STEP:", "").strip()
        for line in raw.split("\n")
        if line.strip().startswith("STEP:")
    ]

    if not steps:
        steps = [raw.strip()]

    return {
        "steps": steps
    }