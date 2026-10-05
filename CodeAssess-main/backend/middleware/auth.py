from functools import wraps
from flask import request, jsonify, g
from firebase_admin import auth as firebase_auth

def require_auth(f):
    """
    Decorator to protect routes. Verifies the Firebase ID token sent in the Authorization header.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "Unauthorized. Authorization token required."}), 401
        
        token = auth_header.split('Bearer ')[1]
        try:
            # Verify the ID token. Check if it is expired or revoked.
            decoded_token = firebase_auth.verify_id_token(token)
            # Store user data in Flask's global request context
            g.user = {
                "uid": decoded_token.get("uid"),
                "email": decoded_token.get("email"),
                "admin": decoded_token.get("admin", False)
            }
        except firebase_auth.ExpiredIdTokenError:
            return jsonify({"error": "Unauthorized. Token has expired."}), 401
        except firebase_auth.RevokedIdTokenError:
            return jsonify({"error": "Unauthorized. Token has been revoked."}), 401
        except Exception as e:
            return jsonify({"error": f"Unauthorized. Invalid token: {str(e)}"}), 401
            
        return f(*args, **kwargs)
    return decorated_function

def require_admin(f):
    """
    Decorator to restrict access to Admins only. Must be used AFTER @require_auth.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not hasattr(g, 'user'):
            return jsonify({"error": "Unauthorized. Authentication required first."}), 401
        
        if not g.user.get("admin", False):
            return jsonify({"error": "Forbidden. Admin privileges required."}), 403
            
        return f(*args, **kwargs)
    return decorated_function
