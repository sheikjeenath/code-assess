from flask import Blueprint, jsonify

admin_users_bp = Blueprint('admin_users', __name__)

@admin_users_bp.route('', methods=['GET'])
def get_admin_users():
    # Placeholder for Phase 7
    return jsonify({"users": []}), 200
