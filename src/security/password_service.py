from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

password_hasher = PasswordHasher()


def hash_password(password):
    return password_hasher.hash(password)


def verify_password(stored_hash, password):
    try:
        return password_hasher.verify(stored_hash, password)
    except VerifyMismatchError:
        return False
