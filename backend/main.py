from bug_detector import detect_bug
from runtime_detector import detect_runtime_error

from agents.learning_agent import generate_hint
from agents.repair_agent import repair_code
from agents.explanation_agent import explain_error
from agents.improvement_agent import suggest_improvements
from agents.quiz_agent import generate_quiz

from memory import create_database, save_error
from code_cleaner import clean_code

create_database()

sample_code = """
for i in range(5)
    print(i)
"""


# This will store whichever error is found
error_info = None


# Step 1: Check syntax errors
syntax_error = detect_bug(sample_code)

if syntax_error["error_type"] is not None:
    error_info = syntax_error

else:
    # Step 2: Check runtime errors
    runtime_error = detect_runtime_error(sample_code)

    if runtime_error["error_type"] is not None:
        error_info = runtime_error


# If any error is detected, run all agents
if error_info is not None:
    
    save_error(error_info)

    print("Error Detected:")
    print(error_info)
    


    # Learning Agent
    hint_result = generate_hint(error_info)
    print(hint_result)


    # Repair Agent
    repair_result = repair_code(
        sample_code,
        error_info
    )

    # Clean LLM output
    repair_result["fixed_code"] = clean_code(
        repair_result["fixed_code"]
    )

    print(repair_result)


    # Explanation Agent
    explanation_result = explain_error(error_info)
    print(explanation_result)


    # Improvement Agent
    improvement_result = suggest_improvements(
        sample_code,
        repair_result["fixed_code"]
    )

    print(improvement_result)


    # Quiz Agent
    quiz_result = generate_quiz(
        error_info,
        explanation_result["explanation"]
    )

    print(quiz_result)


else:

    print("No errors found. Code is running correctly.")
