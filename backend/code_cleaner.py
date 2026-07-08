def clean_code(code):

    code = code.replace("```python", "")
    code = code.replace("```", "")

    return code.strip()