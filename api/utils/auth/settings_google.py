import os

from dotenv import load_dotenv

load_dotenv()


class SettingsGoogleOAuth:
    CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
    REDIRECT_URI = "http://localhost:8000/api/v1/auth/google/callback"
    CERTS_PUBLIC_KEYS = "https://www.googleapis.com/oauth2/v3/certs"
    ACCOUNTS = "https://accounts.google.com",
    GET_TOKENS = "https://oauth2.googleapis.com/token"
    RECEIVE_CODE = "https://accounts.google.com/o/oauth2/v2/auth?"
