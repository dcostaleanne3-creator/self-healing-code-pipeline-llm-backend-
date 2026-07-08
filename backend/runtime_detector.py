def detect_runtime_error(code):
    print("Runtime Detector Activated")

    try:
        exec(code)

        return {
            "error_type": None,
            "message": "No runtime errors found"
        }

    except Exception as e:
        return {
            "error_type": type(e).__name__,
            "message": str(e)
        }