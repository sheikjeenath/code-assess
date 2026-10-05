from functools import wraps
import time
from flask import request, jsonify, g
from config import Config

# Simple in-memory storage for rate limiting: {user_uid: [timestamp1, timestamp2, ...]}
run_limits = {}
submit_limits = {}

def rate_limit_run(f):
    """
    In-memory sliding window rate limiter for code compilation/run requests.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Fallback to remote IP if UID is not set
        user_key = g.user.get("uid") if hasattr(g, 'user') else request.remote_addr
        
        now = time.time()
        window = Config.RATE_LIMIT_RUN_WINDOW
        max_requests = Config.RATE_LIMIT_RUN_MAX
        
        if user_key not in run_limits:
            run_limits[user_key] = []
            
        # Filter timestamps outside the window
        run_limits[user_key] = [t for t in run_limits[user_key] if now - t < window]
        
        if len(run_limits[user_key]) >= max_requests:
            return jsonify({
                "error": "Too Many Requests",
                "message": f"Rate limit exceeded. You can only run code {max_requests} times per minute."
            }), 429
            
        run_limits[user_key].append(now)
        return f(*args, **kwargs)
    return decorated_function

def rate_limit_submit(f):
    """
    In-memory sliding window rate limiter for submissions.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_key = g.user.get("uid") if hasattr(g, 'user') else request.remote_addr
        
        now = time.time()
        window = Config.RATE_LIMIT_SUBMIT_WINDOW
        max_requests = Config.RATE_LIMIT_SUBMIT_MAX
        
        if user_key not in submit_limits:
            submit_limits[user_key] = []
            
        # Filter timestamps
        submit_limits[user_key] = [t for t in submit_limits[user_key] if now - t < window]
        
        if len(submit_limits[user_key]) >= max_requests:
            return jsonify({
                "error": "Too Many Requests",
                "message": f"Rate limit exceeded. You can only submit solutions {max_requests} times per minute."
            }), 429
            
        submit_limits[user_key].append(now)
        return f(*args, **kwargs)
    return decorated_function
