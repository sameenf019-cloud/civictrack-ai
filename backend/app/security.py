from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

_hasher = PasswordHasher()


def hash_password(password: str) -> str:
    """Turns a plain password into a safe hash for the database."""
    return _hasher.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """Checks a plain password against a stored hash."""
    try:
        return _hasher.verify(hashed_password, password)
    except VerifyMismatchError:
        return False