from flask import Flask, request, jsonify

from main import (
    stage_detect,
    stage_hint,
    stage_repair,
    stage_explain,
    stage_improve,
    stage_quiz,
    stage_quiz_answer,
    stage_progress,
    stage_mentor_blocks,
    stage_mentor_explain_block,
    stage_mentor_why_line,
    stage_mentor_what_if,
    stage_mentor_restyle,
    stage_mentor_chat,
    stage_mentor_viva_question,
    stage_mentor_viva_evaluate
)

app = Flask(__name__)


@app.route("/detect", methods=["POST"])
def detect():
    data = request.json
    code = data.get("code", "")
    return jsonify(stage_detect(code))


@app.route("/hint", methods=["POST"])
def hint():
    data = request.json
    code = data.get("code", "")
    error_info = data.get("error_info", {})
    attempts = data.get("attempts", 1)
    return jsonify(stage_hint(code, error_info, attempts))


@app.route("/repair", methods=["POST"])
def repair():
    data = request.json
    code = data.get("code", "")
    error_info = data.get("error_info", {})
    return jsonify(stage_repair(code, error_info))


@app.route("/explain", methods=["POST"])
def explain():
    data = request.json
    error_info = data.get("error_info", {})
    return jsonify(stage_explain(error_info))


@app.route("/improve", methods=["POST"])
def improve():
    data = request.json
    code = data.get("code", "")
    fixed_code = data.get("fixed_code", None)
    return jsonify(stage_improve(code, fixed_code))


@app.route("/quiz", methods=["POST"])
def quiz():
    data = request.json
    error_info = data.get("error_info", {})
    explanation = data.get("explanation", "")
    return jsonify(stage_quiz(error_info, explanation))


@app.route("/quiz-answer", methods=["POST"])
def quiz_answer():
    data = request.json
    quiz_id = data.get("quiz_id")
    selected = data.get("selected")
    return jsonify(stage_quiz_answer(quiz_id, selected))


@app.route("/progress", methods=["GET"])
def progress():
    return jsonify(stage_progress())


@app.route("/mentor/blocks", methods=["POST"])
def mentor_blocks():
    data = request.json
    code = data.get("code", "")
    return jsonify(stage_mentor_blocks(code))


@app.route("/mentor/explain-block", methods=["POST"])
def mentor_explain_block():
    data = request.json
    code = data.get("code", "")
    index = data.get("index", 1)
    return jsonify(stage_mentor_explain_block(code, index))


@app.route("/mentor/why-line", methods=["POST"])
def mentor_why_line():
    data = request.json
    code = data.get("code", "")
    selected_text = data.get("selected_text", "")
    return jsonify(stage_mentor_why_line(code, selected_text))


@app.route("/mentor/what-if", methods=["POST"])
def mentor_what_if():
    data = request.json
    code = data.get("code", "")
    selected_text = data.get("selected_text", "")
    return jsonify(stage_mentor_what_if(code, selected_text))


@app.route("/mentor/restyle", methods=["POST"])
def mentor_restyle():
    data = request.json
    question = data.get("question", "")
    previous_answer = data.get("previous_answer", "")
    style = data.get("style", "simple")
    return jsonify(stage_mentor_restyle(question, previous_answer, style))


@app.route("/mentor/chat", methods=["POST"])
def mentor_chat():
    data = request.json
    code = data.get("code", "")
    history = data.get("history", [])
    question = data.get("question", "")
    return jsonify(stage_mentor_chat(code, history, question))


@app.route("/mentor/viva-question", methods=["POST"])
def mentor_viva_question():
    data = request.json
    code = data.get("code", "")
    asked_so_far = data.get("asked_so_far", [])
    return jsonify(stage_mentor_viva_question(code, asked_so_far))


@app.route("/mentor/viva-evaluate", methods=["POST"])
def mentor_viva_evaluate():
    data = request.json
    code = data.get("code", "")
    question = data.get("question", "")
    student_answer = data.get("student_answer", "")
    return jsonify(stage_mentor_viva_evaluate(code, question, student_answer))


if __name__ == "__main__":
    app.run(port=5000, threaded=True)