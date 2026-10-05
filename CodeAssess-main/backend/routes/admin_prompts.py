from flask import Blueprint, jsonify

admin_prompts_bp = Blueprint('admin_prompts', __name__)

@admin_prompts_bp.route('', methods=['GET'])
def get_admin_prompts():
    # Placeholder for Phase 7
    return jsonify({"prompts": []}), 200
