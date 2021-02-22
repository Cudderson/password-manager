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


def store_master_key(new_master_key):

    master_key_query = 'INSERT INTO Master (master_key) VALUES (%s)'

    new_master_key = encrypt_password(new_master_key.encode('UTF-8'))

    db.cursor.execute(master_key_query, (new_master_key,))
    db.pm_db.commit()


def master_login(master_from_db):
    """Retrieves master key and allows access to db if matched correctly"""

    login_master = input("\nEnter your master password to begin using Password Manager: ")

    if login_master == master_from_db:

        print("Access granted!\n")
        access_granted = True

        return access_granted

    else:
        # get master, and decrypt/decode
        print("Uh oh, that is not your master password. Try again.")
        return master_login()


# make sure database is set up correctly
def confirm_tables_existence():
    """Ensures user's database has proper schema for using program"""

    if db.tables_exist():
        print("database found...")
    else:
        db.create_tables()
        print("database schema created successfully.")
        db.store_encryption_key()
        print("encryption key created and stored")


def confirm_master_existence():
    """
    Ensures the user has a master password for accessing database.
    Returns the master key for login.
    """

    master_exists_query = 'SELECT * FROM master'
    db.cursor.execute(master_exists_query)
    master_exists = db.cursor.fetchone()

    if master_exists:
        # queue log in
        print('it exists')
        my_master = get_master_key()
        my_master = decrypt_password(my_master).decode()

    else:
        # create master password
        print('it does not exist')
        new_master = master_key.create_master_key()
        store_master_key(new_master)
        my_master = get_master_key()
        my_master = decrypt_password(my_master).decode()

    return my_master


confirm_tables_existence()
confirm_master_existence()
master_login(confirm_master_existence())

