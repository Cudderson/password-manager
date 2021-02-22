"""This file will be the main script for program"""

import db
import master_key
from cryptography.fernet import Fernet

print("hello world!")

input() # wait for db connection


def get_crypt_key():
    """Retrieves crypt key from file"""

    with open('crypt_key.txt', 'rb') as f:
        my_key = f.read()

    # returns instantiation of the key (cipher)
    return Fernet(my_key)


def encrypt_password(password_to_encrypt):
    """Encrypts data for database"""

    fk = get_crypt_key()
    encrypted_password = fk.encrypt(password_to_encrypt)

    return encrypted_password


def decrypt_password(password_to_decrypt):
    """Decrypts data from database"""

    fk = get_crypt_key()

    decrypted_password = fk.decrypt(password_to_decrypt)

    return decrypted_password


def get_master_key():
    """Retrieves, decrypts, and returns master key from db"""

    get_master_query = 'SELECT master.master_key ' \
                       'FROM master ' \
                       'WHERE master.master_key_id = 1'

    db.cursor.execute(get_master_query)
    master_key_found = db.cursor.fetchone()

    master_key_found = master_key_found[0].encode()

    return master_key_found


def store_master_key():
    # create master key
    new_master, master_key_query = master_key.create_master_key()

    new_master = encrypt_password(new_master.encode('UTF-8'))

    db.cursor.execute(master_key_query, (new_master,))
    db.pm_db.commit()


store_master_key() # still need to encrypt the master key
print("master key created and stored")
x = get_master_key()
print(f"master key from db, decrypted >> {x}")


