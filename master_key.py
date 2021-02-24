"""File that handles the creation of the master key, as well as retrieving it"""

import db
import crypt_utils


def create_master_key():
    """Creates and returns master password"""

    print("\nBefore we begin, let's set a master password for this program.\n"
          "Your master password will be required to access your stored passwords.")

    new_master = input("\nEnter your new master password: ")
    new_master_confirm = input("To confirm, enter your new master password again: ")

    if new_master == new_master_confirm:

        store_new_master_confirm = input(f"\nStore new master password '{new_master}' ? (yes/no): ")

        if store_new_master_confirm == 'yes':

            return new_master

        elif store_new_master_confirm == 'no':

            print("\nNew master password was not created. To use Password Manager, you must create one.")
            return create_master_key()

        else:
            print("\nCommand not recognized. No changes were made.")
            return create_master_key()
    else:
        print("\nPasswords did not match. Nothing was altered.")
        return create_master_key()


def store_master_key(new_master_key, key):

    master_key_query = 'INSERT INTO Master (master_key) VALUES (%s)'

    new_master_key = crypt_utils.encrypt_password(new_master_key.encode('UTF-8'), key)

    db.cursor.execute(master_key_query, (new_master_key,))
    db.pm_db.commit()


def get_master_key():
    """Retrieves, decrypts, and returns master key from db"""

    get_master_query = 'SELECT master.master_key ' \
                       'FROM master ' \
                       'WHERE master.master_key_id = 1'

    db.cursor.execute(get_master_query)
    master_key_found = db.cursor.fetchone()

    master_key_found = master_key_found[0].encode()

    return master_key_found


def confirm_master_existence(key):
    """
    Ensures the user has a master password for accessing database.
    Returns the master key for login.
    """

    master_exists_query = 'SELECT * FROM master'
    db.cursor.execute(master_exists_query)
    master_exists = db.cursor.fetchone()

    if master_exists:
        # queue log in
        my_master = get_master_key()
        my_master = crypt_utils.decrypt_password(my_master, key).decode()

    else:
        # create master password
        new_master = create_master_key()
        store_master_key(new_master, key)
        my_master = get_master_key()
        my_master = crypt_utils.decrypt_password(my_master, key).decode()

    return my_master
