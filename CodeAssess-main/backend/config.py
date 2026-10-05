import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    PORT = int(os.getenv("PORT", 5000))
    ENV = os.getenv("FLASK_ENV", "development")
    DEBUG = ENV == "development"
    
    # Firebase Service Account
    # Can point to a file path containing serviceAccountKey.json
    FIREBASE_SERVICE_ACCOUNT_PATH = os.getenv("FIREBASE_SERVICE_ACCOUNT_PATH", "")
    
    # Judge0 Config
    # If using RapidAPI: https://judge0-ce.p.rapidapi.com
    # If self-hosted: http://localhost:2358
    JUDGE0_API_URL = os.getenv("JUDGE0_API_URL") or "http://localhost:2358"
    # Required for RapidAPI, empty for local/self-hosted
    JUDGE0_API_KEY = os.getenv("JUDGE0_API_KEY", "")
    
    # Gemini AI Config
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    
    # Security Configs
    JWT_ALGORITHM = "RS256"
    
    # Optional Rate Limiting (seconds)
    RATE_LIMIT_RUN_WINDOW = 60
    RATE_LIMIT_RUN_MAX = 10
    RATE_LIMIT_SUBMIT_WINDOW = 60
    RATE_LIMIT_SUBMIT_MAX = 5
