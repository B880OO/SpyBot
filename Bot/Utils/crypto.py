from cryptography.fernet import Fernet, InvalidToken
from Bot.config import settings

fernet = Fernet(settings.FERNET_KEY.encode())


def encrypt(text: str) -> str:
    if not text:
        return ""
    return fernet.encrypt(text.encode()).decode()


def decrypt(token: str) -> str:
    if not token:
        return ""
    try:
        return fernet.decrypt(token.encode()).decode()
    except InvalidToken:
        return ""
