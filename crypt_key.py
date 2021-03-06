"""File for creation of an encryption key for data handling in database"""

from cryptography.fernet import Fernet


def create_crypt_key():
    """
    Checks mysql table for a Fernet key and stores a newly generated one if it does not exist
    """

    # key is type 'bytes'
    new_crypt_key = Fernet.generate_key()

    return new_crypt_key
