import firebase_admin
from firebase_admin import credentials, firestore, auth
from config import Config
import os

# Initialize Firebase Admin SDK
def initialize_firebase():
    if not firebase_admin._apps:
        cert_path = Config.FIREBASE_SERVICE_ACCOUNT_PATH
        if cert_path and os.path.exists(cert_path):
            cred = credentials.Certificate(cert_path)
            firebase_admin.initialize_app(cred)
            print(f"Firebase initialized successfully with credentials file at {cert_path}")
        else:
            # Fallback to default application credentials
            try:
                firebase_admin.initialize_app()
                print("Firebase initialized with default application credentials")
            except Exception as e:
                # If we are in local dev, allow dummy initialization or log warning
                print(f"WARNING: Firebase initialization failed. Firestore operations will error. Details: {e}")
                # We will still try to run without crashing, but print instructions.
                raise e

# Initialize database client
initialize_firebase()
db = firestore.client()
