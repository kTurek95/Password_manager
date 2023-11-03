import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def create_key(password):
    salt = b'asdfghhgfdsa'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390000
    )

    key = base64.urlsafe_b64encode(kdf.derive(password.encode('utf-8')))
    return key


def encrypt_password(password, website_password):
    key = create_key(password)
    fernet = Fernet(key)

    if isinstance(website_password, bytes):
        encrypted_password = fernet.encrypt(website_password)
    else:
        encrypted_password = fernet.encrypt(website_password.encode('utf-8'))

    return encrypted_password


def decrypt_password(password, website_password):
    password_to_decrypt = website_password
    key = create_key(password)
    fernet = Fernet(key)
    decrypted_password = fernet.decrypt(password_to_decrypt).decode('utf-8')

    return decrypted_password