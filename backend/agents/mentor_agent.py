from agents.llm_client import ask_llm
import json
import re


def split_into_blocks(code):
    """Split code into blank-line-separated blocks (roughly one function/section each)."""

    lines = code.split("\n")
    blocks = []
    current = []

    for line in lines:
        if line.strip() == "":
            if current:
                blocks.append("\n".join(current))
                current = []
        else:
            current.append(line)

    if current:
        blocks.append("\n".join(current))

    return blocks if blocks else [code]


def explain_block(block_code, block_index, total_blocks):

    print(f"Mentor: explaining block {block_index}/{total_blocks}")

    prompt = f"""
You are a friendly Python mentor explaining code to a beginner, one section at a time.

This is section {block_index} of {total_blocks} in the student's program:

{block_code}

Explain what this section does in simple, beginner-friendly language.
Keep it to 3-5 sentences. Do not restate the code, just explain its purpose and behavior.
"""

    explanation = ask_llm(prompt)

    return {
        "block_code": block_code,
        "explanation": explanation,
        "index": block_index,
        "total": total_blocks
    }


def why_this_line(full_code, selected_text):

    print("Mentor: why this line")

    prompt = f"""
You are a friendly Python mentor.

Full program for context:
{full_code}

The student pointed at this specific part and wants to understand it:
{selected_text}

Answer in exactly this structure, plain text, no markdown symbols:

What: <one sentence on what it does>
Why: <one sentence on why it's needed/used here>
Without it: <one sentence on what would go wrong or change if removed>

Keep each line short and beginner-friendly.
"""

    return {"answer": ask_llm(prompt)}


def what_if_removed(full_code, selected_text):

    print("Mentor: what if removed")

    prompt = f"""
You are a friendly Python mentor.

Full program for context:
{full_code}

The student wants to know what would happen if this part were removed or changed:
{selected_text}

Explain, in 2-3 beginner-friendly sentences, what would actually happen if this were
removed (would it error, behave differently, or still work but worse?). Be concrete
and specific to this code, not generic.
"""

    return {"answer": ask_llm(prompt)}


def restyle_answer(original_question, previous_answer, style):

    print(f"Mentor: restyling answer as '{style}'")

    style_instructions = {
        "technical": "Explain it precisely and technically, using correct terminology, as you would to a CS student.",
        "simple": "Explain it in the simplest possible everyday language, avoiding jargon entirely.",
        "story": "Explain it using a short real-life analogy or story that makes the concept memorable."
    }

    instruction = style_instructions.get(style, style_instructions["simple"])

    prompt = f"""
A student asked: {original_question}

A previous answer was given: {previous_answer}

The student wants the SAME question answered differently. {instruction}

Keep it to 3-5 sentences. Do not mention that this is a "restyled" answer, just answer naturally.
"""

    return {"answer": ask_llm(prompt)}


def doubt_chat(code, conversation_history, question):

    print("Mentor: doubt corner chat")

    history_text = ""
    for turn in conversation_history:
        history_text += f"Student: {turn['question']}\nMentor: {turn['answer']}\n\n"

    prompt = f"""
You are a friendly, patient Python mentor, available inside the student's code editor
to answer ANY question they have about their program, at any time.

The student's current code:
{code}

Conversation so far:
{history_text}

The student now asks:
{question}

Answer clearly and concisely, in a beginner-friendly way, grounded in their actual code
where relevant. 2-5 sentences unless genuinely more detail is needed.
"""

    return {"answer": ask_llm(prompt)}


def generate_viva_question(code, asked_so_far):

    print("Mentor: generating Viva question")

    asked_text = "\n".join(f"- {q}" for q in asked_so_far) if asked_so_far else "None yet."

    prompt = f"""
You are an examiner conducting a friendly viva (oral exam) about this student's Python program:

{code}

Questions already asked:
{asked_text}

Ask ONE new question about their code — something that tests whether they understand
WHY they wrote something a certain way, not just what it does. Do not repeat a previous question.

Respond with only the question text, nothing else.
"""

    question = ask_llm(prompt)

    return {"question": question.strip()}


def evaluate_viva_answer(code, question, student_answer):

    print("Mentor: evaluating Viva answer")

    prompt = f"""
You are an examiner evaluating a student's answer in a Python viva.

Their program:
{code}

Question asked:
{question}

Student's answer:
{student_answer}

Respond ONLY with valid JSON in this exact format:

{{
  "verdict": "correct" or "partially correct" or "incorrect",
  "feedback": "1-2 sentence friendly feedback on their answer",
  "ideal_answer": "a concise ideal answer to the question"
}}
"""

    raw = ask_llm(prompt)

    match = re.search(r"\{.*\}", raw, re.DOTALL)
    json_text = match.group(0) if match else raw

    try:
        return json.loads(json_text)
    except Exception:
        return {
            "verdict": "partially correct",
            "feedback": "Thanks for your answer — here's the ideal response for comparison.",
            "ideal_answer": raw.strip()
        }