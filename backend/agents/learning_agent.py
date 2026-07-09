from agents.llm_client import ask_llm
from memory import get_error_count


def generate_hint(error_info):

    print("Learning Agent Activated")

    error_type = error_info["error_type"]
    message = error_info["message"]
    
    previous_count = get_error_count(
    error_info["error_type"]
)
    prompt = f"""
The developer has previously encountered
{error_info["error_type"]}
{previous_count} times.

If previous_count is greater than 3,
explicitly mention that this is a recurring issue.

For recurring issues:
- provide a longer hint
- remind the developer of the underlying concept
- explain common situations where this mistake occurs

Error Type:
{error_info["error_type"]}

Message:
{error_info["message"]}

Provide only a hint.
Do not provide the full solution.
"""

    hint = ask_llm(prompt)

    return {
        "hint": hint
    }