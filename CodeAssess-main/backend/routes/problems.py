from flask import Blueprint, request, jsonify, g
from services.firebase_service import db
from middleware.auth import require_auth, require_admin
import time

problems_bp = Blueprint('problems', __name__)

@problems_bp.route('', methods=['GET'])
@require_auth
def get_problems():
    """
    Get all problems. Users only see enabled problems.
    Admins see all problems (both enabled and disabled).
    """
    try:
        problems_ref = db.collection('problems')
        
        # If user is admin, fetch all, otherwise filter by enabled=True
        is_admin = g.user.get("admin", False)
        
        if is_admin:
            docs = problems_ref.stream()
        else:
            docs = problems_ref.where('enabled', '==', True).stream()
            
        problems_list = []
        for doc in docs:
            p_data = doc.to_dict()
            # Ensure ID is included
            p_data['id'] = doc.id
            # Remove hiddenTestCases if they were accidentally stored at top-level
            p_data.pop('hiddenTestCases', None)
            problems_list.append(p_data)
            
        return jsonify({"problems": problems_list}), 200
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500

@problems_bp.route('/<problem_id>', methods=['GET'])
@require_auth
def get_problem(problem_id):
    """
    Get details of a single problem.
    """
    try:
        doc_ref = db.collection('problems').document(problem_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            return jsonify({"error": "Not Found", "message": "Problem not found."}), 404
            
        p_data = doc.to_dict()
        p_data['id'] = doc.id
        p_data.pop('hiddenTestCases', None)
        
        # Access control: standard user cannot view disabled problems
        is_admin = g.user.get("admin", False)
        if not is_admin and not p_data.get('enabled', True):
            return jsonify({"error": "Forbidden", "message": "Access to this problem is disabled."}), 403
            
        return jsonify(p_data), 200
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500

@problems_bp.route('', methods=['POST'])
@require_auth
@require_admin
def create_problem():
    """
    Create a new problem (Admin only).
    """
    data = request.get_json(silent=True) or {}
    required_fields = ['id', 'title', 'description', 'difficulty', 'tags', 'starterTemplates']
    
    # Validation
    for field in required_fields:
        if field not in data:
            return jsonify({"error": "Bad Request", "message": f"Field '{field}' is required."}), 400
            
    problem_id = data['id'].strip().lower().replace(' ', '-')
    
    try:
        doc_ref = db.collection('problems').document(problem_id)
        if doc_ref.get().exists:
            return jsonify({"error": "Conflict", "message": "Problem with this ID already exists."}), 409
            
        # Structure payload
        payload = {
            "title": data['title'],
            "description": data['description'],
            "difficulty": data['difficulty'],
            "tags": data['tags'] if isinstance(data['tags'], list) else [data['tags']],
            "starterTemplates": data['starterTemplates'],
            "constraints": data.get('constraints', []),
            "sampleCases": data.get('sampleCases', []),
            "enabled": data.get('enabled', True),
            "createdAt": time.time(),
            "updatedAt": time.time()
        }
        
        doc_ref.set(payload)
        
        # If hidden test cases are supplied, write them to subcollection
        hidden_cases = data.get('hiddenTestCases', [])
        for i, tc in enumerate(hidden_cases):
            tc_ref = doc_ref.collection('hiddenTestCases').document(f"tc_{i+1}")
            tc_ref.set({
                "input": tc.get("input", ""),
                "output": tc.get("output", ""),
                "isSample": tc.get("isSample", False)
            })
            
        return jsonify({"message": "Problem created successfully", "id": problem_id}), 201
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500

@problems_bp.route('/<problem_id>', methods=['PUT'])
@require_auth
@require_admin
def update_problem(problem_id):
    """
    Update an existing problem (Admin only).
    """
    data = request.get_json(silent=True) or {}
    try:
        doc_ref = db.collection('problems').document(problem_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            return jsonify({"error": "Not Found", "message": "Problem not found."}), 404
            
        # Update allowed fields
        update_fields = {}
        for field in ['title', 'description', 'difficulty', 'tags', 'starterTemplates', 'constraints', 'sampleCases', 'enabled']:
            if field in data:
                update_fields[field] = data[field]
                
        update_fields['updatedAt'] = time.time()
        doc_ref.update(update_fields)
        
        # If hidden test cases are supplied, overwrite the collection
        if 'hiddenTestCases' in data:
            # Delete old test cases
            old_tcs = doc_ref.collection('hiddenTestCases').stream()
            for otc in old_tcs:
                otc.reference.delete()
            # Write new ones
            hidden_cases = data['hiddenTestCases']
            for i, tc in enumerate(hidden_cases):
                tc_ref = doc_ref.collection('hiddenTestCases').document(f"tc_{i+1}")
                tc_ref.set({
                    "input": tc.get("input", ""),
                    "output": tc.get("output", ""),
                    "isSample": tc.get("isSample", False)
                })
                
        return jsonify({"message": "Problem updated successfully", "id": problem_id}), 200
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500

@problems_bp.route('/<problem_id>', methods=['DELETE'])
@require_auth
@require_admin
def delete_problem(problem_id):
    """
    Delete a problem (Admin only).
    """
    try:
        doc_ref = db.collection('problems').document(problem_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            return jsonify({"error": "Not Found", "message": "Problem not found."}), 404
            
        # Delete hidden test cases first
        tcs = doc_ref.collection('hiddenTestCases').stream()
        for tc in tcs:
            tc.reference.delete()
            
        # Delete problem
        doc_ref.delete()
        return jsonify({"message": "Problem deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500

@problems_bp.route('/<problem_id>/testcases', methods=['GET'])
@require_auth
@require_admin
def get_problem_testcases(problem_id):
    """
    Get hidden test cases of a single problem (Admin only).
    """
    try:
        doc_ref = db.collection('problems').document(problem_id)
        if not doc_ref.get().exists:
            return jsonify({"error": "Not Found", "message": "Problem not found."}), 404
            
        tcs_ref = doc_ref.collection('hiddenTestCases')
        docs = tcs_ref.stream()
        
        tcs_list = []
        for doc in docs:
            tc_data = doc.to_dict()
            tc_data['id'] = doc.id
            tcs_list.append(tc_data)
            
        return jsonify({"testCases": tcs_list}), 200
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500
