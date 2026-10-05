import os
from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from middleware.error_handler import register_error_handlers

# Import blueprints
from routes.auth import auth_bp
from routes.problems import problems_bp
from routes.submissions import submissions_bp
from routes.dashboard import dashboard_bp
from routes.admin_users import admin_users_bp
from routes.admin_submissions import admin_submissions_bp
from routes.admin_analytics import admin_analytics_bp
from routes.admin_prompts import admin_prompts_bp

def create_app():
    app = Flask(__name__)
    
    # Enable CORS for React frontend (development and production allowed hosts)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Global error handlers
    register_error_handlers(app)
    
    # Register API blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(problems_bp, url_prefix='/api/v1/problems')
    app.register_blueprint(submissions_bp, url_prefix='/api/v1/submissions')
    app.register_blueprint(dashboard_bp, url_prefix='/api/v1/dashboard')
    
    # Register Admin blueprints
    app.register_blueprint(admin_users_bp, url_prefix='/api/v1/admin/users')
    app.register_blueprint(admin_submissions_bp, url_prefix='/api/v1/admin/submissions')
    app.register_blueprint(admin_analytics_bp, url_prefix='/api/v1/admin/analytics')
    app.register_blueprint(admin_prompts_bp, url_prefix='/api/v1/admin/prompts')

    # Health check route
    @app.route('/api/v1/health', methods=['GET'])
    def health_check():
        import requests
        # Check Judge0 reachability
        judge0_ok = False
        try:
            r = requests.get(f"{Config.JUDGE0_API_URL}/system/info", timeout=2)
            judge0_ok = r.status_code == 200
        except Exception:
            # Alternate check for judge0 base URL status
            try:
                r = requests.get(Config.JUDGE0_API_URL, timeout=2)
                judge0_ok = r.status_code in [200, 404] # Node/RAPIDAPI might return 404 on base path but is online
            except Exception:
                pass
                
        # Check Gemini config
        gemini_ok = bool(Config.GEMINI_API_KEY)
        
        # Check Firebase config
        firebase_ok = False
        try:
            from services.firebase_service import db
            # Simple list collections check to see if firestore client works
            collections = db.collections()
            firebase_ok = True
        except Exception as e:
            print("Firebase health check warning:", e)
            
        return jsonify({
            "status": "healthy",
            "environment": Config.ENV,
            "services": {
                "judge0": "online" if judge0_ok else "offline",
                "gemini_api_key_configured": gemini_ok,
                "firestore_connection": "online" if firebase_ok else "offline"
            }
        }), 200

    return app

app = create_app()

if __name__ == '__main__':
    port = Config.PORT
    print(f"CodeAssess backend starting on port {port} under {Config.ENV} mode...")
    app.run(host='0.0.0.0', port=port, debug=Config.DEBUG)
