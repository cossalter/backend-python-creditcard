import os
import base64
from passlib.context import CryptContext
from cryptography.fernet import Fernet

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

_fernet = Fernet(bytes(os.getenv("CREDITCARD_ENCRYPT_KEY", "").encode()))


def verify_password(plain_password, hashed_password):
    return _pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return _pwd_context.hash(password)


def base64_encode(number: str) -> str:
    return base64.b64encode(number.encode("ascii")).decode("ascii")


def base64_decode(number: str) -> str:
    return base64.b64decode(number.encode("ascii")).decode("ascii")


def encrypt(text: str) -> str:
    return _fernet.encrypt(text.encode())


def decrypt(text: str) -> str:
    return _fernet.decrypt(text).decode()
