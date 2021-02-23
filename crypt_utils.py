"""File contains functions for encrypting/decrypting values"""


def encrypt_password(password_to_encrypt, key):
    """Encrypts data for database"""

    encrypted_password = key.encrypt(password_to_encrypt)

    return encrypted_password


def decrypt_password(password_to_decrypt, key):
    """Decrypts data from database"""

    decrypted_password = key.decrypt(password_to_decrypt)

    return decrypted_password
