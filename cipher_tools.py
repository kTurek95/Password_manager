import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def create_key(password):
    """
       Creates a secure encryption key from a given password using the PBKDF2HMAC algorithm.

       Parameters:
       password (str): The password to be used for generating the encryption key.

       Returns:
       bytes: The generated encryption key, encoded in URL-safe Base64, suitable for secure storage and transmission.

       Description:
       1. Sets a fixed salt value, which helps defend against dictionary attacks using precomputed hashes (rainbow tables).
       2. Initializes a PBKDF2HMAC instance using:
          - the SHA256 hashing algorithm,
          - a key length of 32 bytes,
          - the predefined salt value,
          - and a high iteration count of 390,000, increasing the computational cost for brute-force attacks.
       3. Uses the PBKDF2HMAC to transform the password into a key through a derivation process.
       4. Encodes the derived key using URL-safe Base64, allowing for secure storage and transport.
    """
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
    """
        Encrypts a website password using a derived key from the user's password.

        Parameters:
        password (str): The user's password used to generate an encryption key.
        website_password (str or bytes): The website password to be encrypted. Can be a string or bytes.

        Returns:
        bytes: The encrypted website password, suitable for secure storage.

        Description:
        1. Generates an encryption key from the user's password using the `create_key` function.
        2. Initializes a Fernet object with the generated key.
        3. Checks if the `website_password` is already in bytes, if not, encodes it to bytes.
        4. Encrypts the website password using Fernet encryption, which uses symmetric encryption with the key.
        5. Returns the encrypted password in bytes, ready for secure storage.

        Note:
        The `create_key` function is used here to derive a secure key from the user's password.
        Fernet ensures that encrypted messages are unable to be manipulated or read without the key.
    """
    key = create_key(password)
    fernet = Fernet(key)

    if isinstance(website_password, bytes):
        encrypted_password = fernet.encrypt(website_password)
    else:
        encrypted_password = fernet.encrypt(website_password.encode('utf-8'))

    return encrypted_password


def decrypt_password(password, website_password):
    """
        Decrypts an encrypted website password using the user's password.

        Parameters:
        password (str): The user's password used to generate the decryption key.
        website_password (bytes): The encrypted website password that needs to be decrypted.

        Returns:
        str: The decrypted website password in plain text.

        Description:
        1. Derives a decryption key using the user's password with the `create_key` function.
        2. Initializes a Fernet object with the derived key.
        3. Decrypts the website password using the Fernet object, which uses symmetric encryption.
        4. Decodes the decrypted password from bytes to a UTF-8 string.
        5. Returns the decrypted password as a string.

        Note:
        The encryption key generated in the `create_key` function must match the key used to encrypt the data.
        Fernet is symmetric encryption, so it uses the same key for encryption and decryption.
        The input `website_password` must be in bytes, and it is expected to have been encrypted with the corresponding key.
    """
    password_to_decrypt = website_password
    key = create_key(password)
    fernet = Fernet(key)
    decrypted_password = fernet.decrypt(password_to_decrypt).decode('utf-8')

    return decrypted_password