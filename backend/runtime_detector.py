import threading
import traceback


def detect_runtime_error(code, timeout=3):
    print("Runtime Detector Activated")

    result = {}

    def target():
        try:
            exec(code, {})
            result["error_type"] = None
            result["message"] = "No runtime errors found"
            result["line"] = None
        except Exception as e:
            tb = traceback.extract_tb(e.__traceback__)
            last_frame = tb[-1] if tb else None
            result["error_type"] = type(e).__name__
            result["message"] = str(e)
            result["line"] = last_frame.lineno if last_frame else None

    thread = threading.Thread(target=target)
    thread.daemon = True
    thread.start()
    thread.join(timeout)

    if thread.is_alive():
        return {
            "error_type": "TimeoutError",
            "message": f"Code took longer than {timeout} seconds to run (possible infinite loop)",
            "line": None
        }

    return result