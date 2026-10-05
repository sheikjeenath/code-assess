import time
import logging
from flask import Blueprint, request, jsonify, g
from firebase_admin import firestore

from services.firebase_service import db
import services.judge0_service as judge0_service
import services.ai_service as ai_service
import services.scoring_service as scoring_service

from middleware.auth import require_auth
from middleware.rate_limit import rate_limit_run, rate_limit_submit
from middleware.validation import validate_submission_payload

logger = logging.getLogger(__name__)

submissions_bp = Blueprint('submissions', __name__)

@submissions_bp.route('', methods=['GET'])
@require_auth
def get_submissions():
    """
    Get paginated submissions list for the current user.
    """
    user_id = g.user.get("uid")
    last_doc_id = request.args.get('lastDocId')
    
    try:
        # Try index-based query
        query = db.collection('submissions').where('userId', '==', user_id).order_by('timestamp', direction=firestore.Query.DESCENDING)
        if last_doc_id:
            last_doc_ref = db.collection('submissions').document(last_doc_id)
            last_doc = last_doc_ref.get()
            if last_doc.exists:
                query = query.start_after(last_doc)
        docs = query.limit(20).stream()
        submissions_list = []
        for doc in docs:
            data = doc.to_dict()
            data['id'] = doc.id
            submissions_list.append(data)
            
        return jsonify({"submissions": submissions_list}), 200
    except Exception as e:
        logger.warning("Ordered query failed, falling back to python sorting: %s", e)
        # Fallback query if composite index not built yet
        try:
            query = db.collection('submissions').where('userId', '==', user_id)
            docs = query.stream()
            all_subs = []
            for doc in docs:
                data = doc.to_dict()
                data['id'] = doc.id
                all_subs.append(data)
                
            def get_ts(x):
                ts = x.get('timestamp')
                if hasattr(ts, 'timestamp'): # datetime objects from Firestore
                    return ts.timestamp()
                try:
                    return float(ts or 0)
                except (TypeError, ValueError):
                    return 0.0
                    
            all_subs.sort(key=get_ts, reverse=True)
            
            start_idx = 0
            if last_doc_id:
                for idx, s in enumerate(all_subs):
                    if s['id'] == last_doc_id:
                        start_idx = idx + 1
                        break
            submissions_list = all_subs[start_idx:start_idx+20]
            return jsonify({"submissions": submissions_list}), 200
        except Exception as ex:
            return jsonify({"error": "Internal Server Error", "message": str(ex)}), 500

@submissions_bp.route('/<submission_id>', methods=['GET'])
@require_auth
def get_submission(submission_id):
    """
    Get a single submission by ID. Must be the author or an admin.
    """
    try:
        doc_ref = db.collection('submissions').document(submission_id)
        doc = doc_ref.get()
        if not doc.exists:
            return jsonify({"error": "Not Found", "message": "Submission not found."}), 404
            
        data = doc.to_dict()
        data['id'] = doc.id
        
        # Access control
        is_admin = g.user.get("admin", False)
        if not is_admin and data.get('userId') != g.user.get('uid'):
            return jsonify({"error": "Forbidden", "message": "You are not authorized to view this submission."}), 403
            
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500

@submissions_bp.route('/run', methods=['POST'])
@require_auth
@rate_limit_run
@validate_submission_payload
def run_code():
    """
    Run candidate code against custom stdin input (or first sample test case).
    Does not save to DB or trigger AI review.
    """
    data = request.get_json(silent=True) or {}
    problem_id = data.get("problemId")
    language = data.get("language")
    code = data.get("code")
    stdin = data.get("stdin", "")
    
    try:
        # Load problem to verify existence
        problem_ref = db.collection('problems').document(problem_id)
        problem_doc = problem_ref.get()
        if not problem_doc.exists:
            return jsonify({"error": "Not Found", "message": "Problem not found."}), 404
            
        # Execute code via Judge0
        run_result = judge0_service.execute_code(code, language, stdin)
        
        return jsonify({
            "stdout": run_result.get("stdout", ""),
            "stderr": run_result.get("stderr", ""),
            "compile_output": run_result.get("compile_output", ""),
            "status": run_result.get("status", ""),
            "runtime": run_result.get("runtime", ""),
            "memory": run_result.get("memory")
        }), 200
        
    except Exception as e:
        logger.error("Run code exception: %s", e, exc_info=True)
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500

@submissions_bp.route('/submit', methods=['POST'])
@require_auth
@rate_limit_submit
@validate_submission_payload
def submit_code():
    """
    Submit candidate code. Evaluates against hidden test cases, computes score,
    requests AI review, saves submission, logs stats, and returns response.
    """
    data = request.get_json(silent=True) or {}
    problem_id = data.get("problemId")
    language = data.get("language")
    code = data.get("code")
    
    try:
        # Load problem
        problem_ref = db.collection('problems').document(problem_id)
        problem_doc = problem_ref.get()
        if not problem_doc.exists:
            return jsonify({"error": "Not Found", "message": "Problem not found."}), 404
            
        problem_data = problem_doc.to_dict()
        
        # Access control
        is_admin = g.user.get("admin", False)
        if not is_admin and not problem_data.get('enabled', True):
            return jsonify({"error": "Forbidden", "message": "Access to this problem is disabled."}), 403
            
        # Fetch hidden test cases
        hidden_tcs_ref = problem_ref.collection('hiddenTestCases')
        hidden_tcs_docs = hidden_tcs_ref.stream()
        hidden_tcs = []
        for doc in hidden_tcs_docs:
            tc_data = doc.to_dict()
            tc_data['id'] = doc.id
            hidden_tcs.append(tc_data)
            
        # Fallback to sample cases if no hidden cases are configured
        if not hidden_tcs:
            hidden_tcs = problem_data.get('sampleCases', [])
            
        if not hidden_tcs:
            return jsonify({"error": "Bad Request", "message": "No test cases configured for this problem."}), 400
            
        passed_cases = 0
        total_cases = len(hidden_tcs)
        max_runtime = 0.0
        max_memory = 0
        
        overall_verdict = "Accepted"
        compile_error_output = ""
        runtime_error_output = ""
        
        # Run test cases
        for tc in hidden_tcs:
            stdin = tc.get("input", "")
            expected_output = tc.get("output", "").strip()
            
            try:
                res = judge0_service.execute_code(code, language, stdin)
            except Exception as e:
                res = {
                    "status": "Runtime Error",
                    "status_id": 16,
                    "stderr": str(e),
                    "stdout": "",
                    "compile_output": "",
                    "runtime": "0.0",
                    "memory": 0
                }
                
            status = res.get("status", "Unknown")
            status_id = res.get("status_id", 0)
            stdout = res.get("stdout", "").strip()
            stderr = res.get("stderr", "")
            compile_output = res.get("compile_output", "")
            
            # Track resource usage
            try:
                rt = float(res.get("runtime") or 0.0)
                if rt > max_runtime:
                    max_runtime = rt
            except ValueError:
                pass
                
            try:
                mem = int(res.get("memory") or 0)
                if mem > max_memory:
                    max_memory = mem
            except ValueError:
                pass
                
            # Handle compilation failure (status_id = 6 or status = "Compilation Error")
            if status == "Compilation Error" or status_id == 6:
                overall_verdict = "Compilation Error"
                compile_error_output = compile_output or stderr
                break
                
            # Check execution correctness
            if status_id == 5:  # Time Limit Exceeded
                if overall_verdict == "Accepted":
                    overall_verdict = "Time Limit Exceeded"
            elif "Runtime Error" in status or status_id in [11, 12, 13, 14, 15, 16]:
                if overall_verdict == "Accepted":
                    overall_verdict = "Runtime Error"
                    runtime_error_output = stderr
            elif stdout != expected_output:
                if overall_verdict == "Accepted":
                    overall_verdict = "Wrong Answer"
            else:
                passed_cases += 1
                
        # On compile error, return immediately without AI call
        if overall_verdict == "Compilation Error":
            # Save submission even if compilation failed
            sub_ref = db.collection('submissions').document()
            sub_id = sub_ref.id
            
            submission_doc = {
                "problemId": problem_id,
                "problemTitle": problem_data.get("title", ""),
                "userId": g.user.get("uid"),
                "userEmail": g.user.get("email"),
                "language": language,
                "code": code,
                "status": overall_verdict,
                "runtime": max_runtime,
                "memory": max_memory,
                "timestamp": firestore.SERVER_TIMESTAMP,
                "passedCases": 0,
                "totalCases": total_cases,
                "overallScore": 0,
                "compile_output": compile_error_output,
                "scoreBreakdown": {
                    "correctness": {"value": 0, "weight": 0.5},
                    "codeQuality": {"value": 0, "weight": 0.2},
                    "complexity": {"value": 0, "weight": 0.1},
                    "readability": {"value": 0, "weight": 0.1},
                    "optimization": {"value": 0, "weight": 0.1}
                },
                "aiReport": {
                    "explanation": "AI analysis skipped due to compilation error.",
                    "improvedCode": code,
                    "improvementExplanation": "",
                    "flowchartMermaid": "graph TD\n  A[Start] --> B[Compilation Error]"
                }
            }
            
            sub_ref.set(submission_doc)
            
            # Log execution stats
            stats_ref = db.collection('executionStats').document()
            stats_ref.set({
                "submissionId": sub_id,
                "problemId": problem_id,
                "language": language,
                "runtime": max_runtime,
                "memory": max_memory,
                "verdict": overall_verdict,
                "timestamp": firestore.SERVER_TIMESTAMP
            })
            
            # Add id for response serialization
            submission_doc["id"] = sub_id
            submission_doc["timestamp"] = time.time()
            return jsonify(submission_doc), 200
            
        # If it compiles, call AI service and compute score
        ai_report = ai_service.analyze_code(
            code=code,
            language=language,
            problem_title=problem_data.get("title", ""),
            problem_description=problem_data.get("description", "")
        )
        
        score_res = scoring_service.compute_overall_score(
            passed_cases=passed_cases,
            total_cases=total_cases,
            ai_report=ai_report
        )
        
        overall_score = score_res.get("overallScore", 0)
        score_breakdown = score_res.get("scoreBreakdown", {})
        
        # Save submission
        sub_ref = db.collection('submissions').document()
        sub_id = sub_ref.id
        
        submission_doc = {
            "problemId": problem_id,
            "problemTitle": problem_data.get("title", ""),
            "userId": g.user.get("uid"),
            "userEmail": g.user.get("email"),
            "language": language,
            "code": code,
            "status": overall_verdict,
            "runtime": max_runtime,
            "memory": max_memory,
            "timestamp": firestore.SERVER_TIMESTAMP,
            "passedCases": passed_cases,
            "totalCases": total_cases,
            "overallScore": overall_score,
            "scoreBreakdown": score_breakdown,
            "aiReport": ai_report
        }
        
        if runtime_error_output:
            submission_doc["stderr"] = runtime_error_output
            
        sub_ref.set(submission_doc)
        
        # Log execution stats
        stats_ref = db.collection('executionStats').document()
        stats_ref.set({
            "submissionId": sub_id,
            "problemId": problem_id,
            "language": language,
            "runtime": max_runtime,
            "memory": max_memory,
            "verdict": overall_verdict,
            "timestamp": firestore.SERVER_TIMESTAMP
        })
        
        # Add id and serialized timestamp for response
        submission_doc["id"] = sub_id
        submission_doc["timestamp"] = time.time()
        
        return jsonify(submission_doc), 200
        
    except Exception as e:
        logger.error("Submission code exception: %s", e, exc_info=True)
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500
