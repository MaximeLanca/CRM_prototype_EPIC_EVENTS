import jwt
from datetime import datetime, timedelta, timezone
from src.models import peewee_models
from dotenv import load_dotenv
import os
from pathlib import Path
from playhouse.db_url import connect

load_dotenv()
DB_URL = os.environ["APP_DB_URL"]
JWT_SECRET = os.environ["APP_JWT_SECRET"]
ALGORITHM = os.environ["ALGORITHM"]
SESSION_FILE = Path.home() / ".epic_events_token"


def generate_token(user):
    date_now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user.id__),
        "role": user.role,
        "iat": int(date_now.timestamp()),
        "exp": int((date_now + timedelta(hours=1)).timestamp()),
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=ALGORITHM)
    print(f"DEBUG generate type: {type(token)} valeur: {token}")
    return token


def decode_token(token) -> dict:
    # if isinstance(token, str):
    #     token = token.encode("utf-8")
    payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
    return payload


def save_token(token):
    SESSION_FILE.write_text(token)


def load_token():
    if not SESSION_FILE.exists():
        return None
    token = SESSION_FILE.read_text().strip()
    return token


def clear_token():
    if SESSION_FILE.exists():
        SESSION_FILE.unlink()
