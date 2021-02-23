"""This file will be the main script for program"""

import db
import master_key
from cryptography.fernet import Fernet
import crypt_utils
import login

print("hello world!")

input() # wait for db connection


def get_crypt_key():
    """Retrieves crypt key from file"""

    with open('crypt_key.txt', 'rb') as f:
        my_key = f.read()

    # returns instantiation of the key (cipher)
    return Fernet(my_key)





key = get_crypt_key()

db.connect_to_database()
db.confirm_tables_existence()
master_key.confirm_master_existence(key)
login.master_login(master_key.confirm_master_existence(key))

# encrypt something
xx = input("Value to encrypt: ").encode("UTF-8")
key = get_crypt_key()
encrypted_val = crypt_utils.encrypt_password(xx, key)
print(encrypted_val)
decrypted_val = crypt_utils.decrypt_password(encrypted_val, key)
print(decrypted_val.decode())

