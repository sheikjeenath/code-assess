import logging
from flask import jsonify
from werkzeug.exceptions import HTTPException

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger("CodeAssessErrorHandler")

def register_error_handlers(app):
    """
    Registers global error handlers on the Flask app.
    """
    @app.errorhandler(Exception)
    def handle_exception(e):
        # Pass HTTPExceptions through
        if isinstance(e, HTTPException):
            logger.warning(f"HTTPException occurred: {e.description} (Status: {e.code})")
            return jsonify({
                "error": e.name,
                "message": e.description
            }), e.code

        # Log details of unexpected errors internally
        logger.exception("Unexpected error occurred!")
        
        # Return generic message to prevent leaking tracebacks
        return jsonify({
            "error": "Internal Server Error",
            "message": "An unexpected error occurred. Please contact the administrator if this persists."
        }), 500
