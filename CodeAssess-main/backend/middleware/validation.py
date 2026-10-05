from functools import wraps
from flask import request, jsonify

def validate_submission_payload(f):
    """
    Validates the structure and content of code execution and submission requests.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "Bad Request", "message": "Invalid or missing JSON payload."}), 400
            
        code = data.get("code")
        language = data.get("language")
        problem_id = data.get("problemId")
        
        # Validation checks
        if not code or not isinstance(code, str) or not code.strip():
            return jsonify({"error": "Bad Request", "message": "Code content is required."}), 400
            
        if not language or not isinstance(language, str) or not language.strip():
            return jsonify({"error": "Bad Request", "message": "Programming language is required."}), 400
            
        # Standardize language identifier
        supported_languages = ["python", "cpp", "java", "javascript"]
        if language.lower() not in supported_languages:
            return jsonify({
                "error": "Bad Request", 
                "message": f"Unsupported language '{language}'. Supported: {', '.join(supported_languages)}"
            }), 400
            
        if not problem_id or not isinstance(problem_id, str) or not problem_id.strip():
            return jsonify({"error": "Bad Request", "message": "Problem ID is required."}), 400
            
        return f(*args, **kwargs)
    return decorated_function
