from bug_detector import detect_bug
from runtime_detector import detect_runtime_error


def validate_repair(fixed_code):

    syntax_result = detect_bug(fixed_code)

    if syntax_result["error_type"] is not None:
        return {
            "valid": False,
            "reason": syntax_result
        }

    runtime_result = detect_runtime_error(fixed_code)

    if runtime_result["error_type"] is not None:
        return {
            "valid": False,
            "reason": runtime_result
        }

    return {
        "valid": True
    }