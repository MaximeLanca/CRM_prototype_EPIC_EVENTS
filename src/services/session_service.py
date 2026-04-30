import click
from src.security.token_service import load_token, clear_token, decode_token
import jwt
from src.security.token_service import generate_token, save_token

class SessionService:
    def __init__(self):
        pass

    def get_payload(self):
        token = load_token()
        if not token:
            return None, "Not logged in"
        try:
            payload = decode_token(token)
            return payload, None
        except jwt.ExpiredSignatureError:
            clear_token()
            return None, "Session expired."
        except jwt.InvalidTokenError:
            clear_token()
            return None, "Invalid token."

    def generate_token(self, user):
        token = self.generate_token(user)
        save_token(token)
        return token

