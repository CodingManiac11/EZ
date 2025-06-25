import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()

FERNET_KEY = os.getenv('FERNET_KEY', 'superfernetkey1234567890123456==')
fernet = Fernet(FERNET_KEY)

def encrypt_id(file_id: int) -> str:
    return fernet.encrypt(str(file_id).encode()).decode()

def decrypt_id(token: str) -> int:
    return int(fernet.decrypt(token.encode()).decode()) 