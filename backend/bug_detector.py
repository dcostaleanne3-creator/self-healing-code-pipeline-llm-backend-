def detect_bug(code):
    print("Analyzing code...")

    try:
        compile(code, "<string>", "exec")

        return {
            "error_type": None,
            "message": "No errors found",
            "line": None
        }

    except Exception as e:
        return {
            "error_type": type(e).__name__,
            "message": str(e),
            "line": getattr(e, "lineno", None)
        }