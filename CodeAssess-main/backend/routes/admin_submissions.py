from flask import Blueprint, jsonify

admin_submissions_bp = Blueprint('admin_submissions', __name__)

@admin_submissions_bp.route('', methods=['GET'])
def get_admin_submissions():
    # Placeholder for Phase 7
    return jsonify({"submissions": []}), 200
