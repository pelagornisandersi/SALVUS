from cryptography.fernet import Fernet
import hashlib
import base64


def room_code_to_key(room_code):
    digest = hashlib.sha256(room_code.encode()).digest()
    return base64.urlsafe_b64encode(digest)


def encrypt_file(file_path, key):
    fernet = Fernet(key)

    with open(file_path, "rb") as file:
        data = file.read()

    encrypted = fernet.encrypt(data)

    return encrypted


def decrypt_data(data, key):
    fernet = Fernet(key)
    return fernet.decrypt(data)