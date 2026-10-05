from flask import Blueprint, request, jsonify, g
from firebase_admin import auth as firebase_auth
from middleware.auth import require_auth
from config import Config

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/make-admin', methods=['POST'])
@require_auth
def make_admin():
    """
    Utility endpoint to set admin privileges for a user.
    In development, anyone can make themselves admin.
    In production, this should require admin authorization or a master secret key.
    """
    uid = g.user.get("uid")
    
    # Check master secret key or allow in dev env
    secret_key = request.headers.get("X-Admin-Secret-Key")
    is_dev = Config.ENV == "development"
    
    # Standard security check
    if not is_dev and secret_key != os.getenv("ADMIN_SECRET_KEY"):
         return jsonify({"error": "Forbidden", "message": "Invalid master administrative secret key."}), 403
         
    try:
        # Set custom claims
        firebase_auth.set_custom_user_claims(uid, {'admin': True})
        return jsonify({
            "message": "Success", 
            "details": f"Admin claims granted to user {uid}. Note: you must sign out and sign back in to refresh claims on frontend."
        }), 200
    except Exception as e:
        return jsonify({"error": "Internal Error", "message": str(e)}), 500
