from agents.llm_client import ask_llm
import json
import re
import threading


fallback_quizzes = {

    "SyntaxError": {
        "question": "Which line contains a SyntaxError?",
        "options": {
            "A": "for i in range(5):\n    print(i)",
            "B": "for i in range(5)\n    print(i)",
            "C": "x = 5"
        },
        "correct": "B"
    },

    "ZeroDivisionError": {
        "question": "Which line raises ZeroDivisionError?",
        "options": {
            "A": "10/2",
            "B": "10/0",
            "C": "10*2"
        },
        "correct": "B"
    },

    "IndexError": {
        "question": "Which line raises IndexError?",
        "options": {
            "A": "a=[1,2]\nprint(a[1])",
            "B": "a=[1,2]\nprint(a[5])",
            "C": "a=[1,2]\nprint(len(a))"
        },
        "correct": "B"
    },

    "NameError": {
        "question": "Which line raises NameError?",
        "options": {
            "A": "x=5\nprint(x)",
            "B": "print(age)",
            "C": "name='Tom'\nprint(name)"
        },
        "correct": "B"
    },

    "TypeError": {
        "question": "Which line raises TypeError?",
        "options": {
            "A": "print('5'+5)",
            "B": "print('5'+'5')",
            "C": "print(5+5)"
        },
        "correct": "A"
    },

    "ValueError": {
        "question": "Which line raises ValueError?",
        "options": {
            "A": "int('123')",
            "B": "int('hello')",
            "C": "float('3.14')"
        },
        "correct": "B"
    },

    "KeyError": {
        "question": "Which line raises KeyError?",
        "options": {
            "A": "d={'a':1}\nprint(d['a'])",
            "B": "d={'a':1}\nprint(d['b'])",
            "C": "print(len(d))"
        },
        "correct": "B"
    },

    "AttributeError": {
        "question": "Which line raises AttributeError?",
        "options": {
            "A": "x='hello'\nprint(x.upper())",
            "B": "x=5\nprint(x.upper())",
            "C": "print(len('hello'))"
        },
        "correct": "B"
    },

    "IndentationError": {
        "question": "Which code snippet causes an IndentationError?",
        "options": {
            "A": "if True:\n    print('hi')",
            "B": "if True:\nprint('hi')",
            "C": "x=5\nprint(x)"
        },
        "correct": "B"
    }
}


def generate_quiz(error_info, explanation):

    print("Quiz Agent Activated")

    error_type = error_info["error_type"]
    message = error_info["message"]

    max_attempts = 3

    for _ in range(max_attempts):

        quiz_data = _generate_quiz_raw(
            error_type,
            message,
            explanation
        )

        if quiz_data is None:
            continue

        verified_data, is_valid = _validate_and_correct(
            quiz_data,
            error_type
        )

        if is_valid:
            return verified_data

    print("Using fallback quiz")

    return fallback_quizzes.get(
        error_type,
        {
            "question": f"Which code snippet is most likely to raise {error_type}?",
            "options": {
                "A": "Option A",
                "B": "Option B",
                "C": "Option C"
            },
            "correct": "A"
        }
    )


def _generate_quiz_raw(
    error_type,
    message,
    explanation
):

    prompt = f"""
You are a Python tutor.

Create a beginner level concept quiz for:

Error Type:
{error_type}

Rules:
- One multiple choice question.
- Three options only.
- Exactly one correct answer.
- The correct option must actually raise {error_type}.
- The other two should not raise this error.
- IMPORTANT: write each option as REAL, properly formatted Python code with
  actual line breaks and indentation preserved using \\n inside the JSON string.
  Do NOT squeeze multi-line code onto one line using semicolons. This matters
  most for IndentationError, where the indentation itself must be visible.
- Return only JSON.

Format:

{{
"question":"...",
"options":{{
"A":"...",
"B":"...",
"C":"..."
}},
"correct":"A"
}}
"""

    raw = ask_llm(prompt)

    match = re.search(
        r"\{.*\}",
        raw,
        re.DOTALL
    )

    json_text = match.group(0) if match else raw

    try:
        return json.loads(json_text)
    except:
        return None


def _run_snippet(code):

    result = {"error": None}

    def target():
        try:
            exec(code, {})
        except Exception as e:
            result["error"] = type(e).__name__

    thread = threading.Thread(
        target=target
    )

    thread.daemon = True
    thread.start()
    thread.join(2)

    if thread.is_alive():
        return "TimeoutError"

    return result["error"]


def _validate_and_correct(
    quiz_data,
    target_error
):

    options = quiz_data["options"]

    matches = []

    for key, code in options.items():

        actual = _run_snippet(code)

        if actual == target_error:
            matches.append(key)

    if len(matches) == 1:
        quiz_data["correct"] = matches[0]
        return quiz_data, True

    return quiz_data, False


def explain_answer(
    question,
    options,
    correct
):

    prompt = f"""
Explain in 2 short sentences why option {correct} is correct.

Question:
{question}

Options:
{options}

Correct:
{correct}

Keep it beginner friendly.
"""

    return ask_llm(prompt)