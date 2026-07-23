from bug_detector import detect_bug
from runtime_detector import detect_runtime_error

from agents.learning_agent import generate_hint
from agents.repair_agent import repair_code
from agents.explanation_agent import explain_error
from agents.improvement_agent import suggest_improvements
from agents.quiz_agent import generate_quiz, explain_answer
from memory import get_progress_data

from memory import (
    create_database,
    save_error,
    save_fix_history,
    save_quiz_result
)

from repair_validator import validate_repair
from code_cleaner import clean_code
from skill_tracker import topic_map

import uuid

create_database()

active_quizzes = {}


def stage_detect(code):

    cleaned_code = clean_code(code)
    error_info = None

    syntax_error = detect_bug(cleaned_code)

    if syntax_error["error_type"] is not None:
        error_info = syntax_error
    else:
        runtime_error = detect_runtime_error(cleaned_code)
        if runtime_error["error_type"] is not None:
            error_info = runtime_error

    if error_info is None:
        return {
            "stage": "success",
            "message": "No errors found. Code is working correctly."
        }

    save_error(error_info)

    return {
        "stage": "error_found",
        "error_type": error_info["error_type"],
        "message": error_info["message"],
        "line": error_info.get("line")
    }


def stage_hint(code, error_info, attempts):

    hint_result = generate_hint(error_info, attempts)

    return {
        "hint": hint_result["hint"],
        "attempts": attempts
    }


def _extract_block(lines, line_no):
    """Find the blank-line-bounded block (usually one function) containing line_no."""

    index = max(0, min(line_no - 1, len(lines) - 1))

    block_start = 0
    for i in range(index, -1, -1):
        if lines[i].strip() == "":
            block_start = i + 1
            break

    block_end = len(lines)
    for i in range(index, len(lines)):
        if lines[i].strip() == "":
            block_end = i
            break

    return block_start, block_end


def stage_repair(code, error_info):

    cleaned_code = clean_code(code)
    line_no = error_info.get("line")

    if not line_no:
        # Fallback: no line number available, repair whole file (old behavior)
        repair_result = repair_code(cleaned_code, error_info)
        fixed_code = clean_code(repair_result["fixed_code"])

    else:
        lines = cleaned_code.split("\n")
        block_start, block_end = _extract_block(lines, line_no)

        block_code = "\n".join(lines[block_start:block_end])

        repair_result = repair_code(block_code, error_info)
        fixed_block = clean_code(repair_result["fixed_code"])

        new_lines = lines[:block_start] + fixed_block.split("\n") + lines[block_end:]
        fixed_code = "\n".join(new_lines)

    validation_result = validate_repair(fixed_code)

    save_fix_history(
        error_info["error_type"],
        cleaned_code,
        fixed_code
    )

    return {
        "fixed_code": fixed_code,
        "validation": validation_result
    }


def stage_explain(error_info):

    result = explain_error(error_info)

    return {
        "steps": result["steps"]
    }


def stage_improve(code, fixed_code=None):

    result = suggest_improvements(code, fixed_code)

    return {
        "suggestions": result["suggestions"]
    }


def stage_quiz(error_info, explanation):

    quiz_data = generate_quiz(error_info, explanation)

    quiz_id = str(uuid.uuid4())

    active_quizzes[quiz_id] = {
        "correct": quiz_data["correct"],
        "topic": topic_map.get(
            error_info["error_type"],
            error_info["error_type"]
        ),
        "question": quiz_data["question"],
        "options": quiz_data["options"]
    }

    return {
        "quiz_id": quiz_id,
        "question": quiz_data["question"],
        "options": quiz_data["options"]
    }


def stage_quiz_answer(quiz_id, selected):

    quiz = active_quizzes.get(quiz_id)

    if not quiz:
        return {"error": "Quiz not found or expired"}

    is_correct = (selected == quiz["correct"])

    save_quiz_result(
        quiz["topic"],
        1 if is_correct else 0
    )

    answer_explanation = explain_answer(
        quiz["question"],
        quiz["options"],
        quiz["correct"]
    )

    del active_quizzes[quiz_id]

    return {
        "correct": is_correct,
        "correct_answer": quiz["correct"],
        "answer_explanation": answer_explanation
    }


def stage_progress():

    data = get_progress_data()

    topics = {}

    for error_type, count in data["error_counts"].items():
        topic_name = topic_map.get(error_type, error_type)
        if topic_name not in topics:
            topics[topic_name] = {"error_count": 0, "attempts": 0, "correct": 0}
        topics[topic_name]["error_count"] += count

    for topic_name, quiz_info in data["quiz_by_topic"].items():
        if topic_name not in topics:
            topics[topic_name] = {"error_count": 0, "attempts": 0, "correct": 0}
        topics[topic_name]["attempts"] += quiz_info["attempts"]
        topics[topic_name]["correct"] += quiz_info["correct"]

    topic_list = []

    for name, info in topics.items():
        if info["attempts"] > 0:
            accuracy = round((info["correct"] / info["attempts"]) * 100)
            status = "tested"
        else:
            accuracy = None
            status = "untested"

        topic_list.append({
            "topic": name,
            "error_count": info["error_count"],
            "attempts": info["attempts"],
            "accuracy": accuracy,
            "status": status
        })

    topic_list.sort(key=lambda t: (t["accuracy"] is None, t["accuracy"] if t["accuracy"] is not None else 0))

    overall_accuracy = (
        round((data["total_quiz_correct"] / data["total_quiz_attempts"]) * 100)
        if data["total_quiz_attempts"] > 0 else None
    )

    return {
        "topics": topic_list,
        "total_errors": data["total_errors"],
        "total_fixes": data["total_fixes"],
        "total_quiz_attempts": data["total_quiz_attempts"],
        "overall_accuracy": overall_accuracy
    }

from agents.mentor_agent import (
    split_into_blocks,
    explain_block,
    why_this_line,
    what_if_removed,
    restyle_answer,
    doubt_chat,
    generate_viva_question,
    evaluate_viva_answer
)


def stage_mentor_blocks(code):
    blocks = split_into_blocks(code)
    return {"total": len(blocks)}


def stage_mentor_explain_block(code, index):
    blocks = split_into_blocks(code)

    if index < 1 or index > len(blocks):
        return {"error": "Invalid block index"}

    return explain_block(blocks[index - 1], index, len(blocks))


def stage_mentor_why_line(code, selected_text):
    return why_this_line(code, selected_text)


def stage_mentor_what_if(code, selected_text):
    return what_if_removed(code, selected_text)


def stage_mentor_restyle(question, previous_answer, style):
    return restyle_answer(question, previous_answer, style)


def stage_mentor_chat(code, history, question):
    return doubt_chat(code, history, question)


def stage_mentor_viva_question(code, asked_so_far):
    return generate_viva_question(code, asked_so_far)


def stage_mentor_viva_evaluate(code, question, student_answer):
    return evaluate_viva_answer(code, question, student_answer)