"""This file will be the main script for program"""

import db
import master_key
from cryptography.fernet import Fernet
import login
import dialogue


def get_crypt_key():
    """Retrieves crypt key from file"""

    with open('crypt_key.txt', 'rb') as f:
        my_key = f.read()

    # returns instantiation of the key (cipher)
    return Fernet(my_key)


def initial_setup():
    """The inital requirements to use the program """
    db.connect_to_database()
    db.confirm_tables_existence()
    key = get_crypt_key()
    master_key.confirm_master_existence(key)
    login.master_login(master_key.confirm_master_existence(key))


def main_dialogue():
    """The main control flow of the program"""

    key = get_crypt_key()

    print("Welcome to Password Manager.\n")
    while True:
        mode = input(
            "Enter a letter to access the corresponding mode:\n"
            "\t- Press 'a' to add a new password\n"
            "\t- Press 'v' to view a password\n"
            "\t- Press 's' to view all sites you have stored\n"
            "\t- Press 'm' to modify an existing password\n"
            "\t- Press 'r' to remove a password from database\n"
            "\t- Press 'q' to quit program\n"
            "\nEnter mode : "
        )

        if mode == 'a':
            dialogue.create_entry(key)
        elif mode == 'v':
            dialogue.view_one_entry(key)
        elif mode == 's':
            db.read_all_entries()
        elif mode == 'm':
            dialogue.modify_password(key)
        elif mode == 'r':
            dialogue.dialogue_delete_entry()
        elif mode == 'q':
            print('Quitting Program.')
            quit()
        else:
            print("Mode not recognized.")


initial_setup()
main_dialogue()
