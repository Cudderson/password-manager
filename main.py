"""This file will be the main script for program"""

import db
import master_key
from cryptography.fernet import Fernet
import crypt_utils
import login
import dialogue

print("hello world!")

input() # wait for db connection


def get_crypt_key():
    """Retrieves crypt key from file"""

    with open('crypt_key.txt', 'rb') as f:
        my_key = f.read()

    # returns instantiation of the key (cipher)
    return Fernet(my_key)


def main_dialogue():
    """The main control flow of the program"""

    print("Welcome to Password Manager.\n")
    while True:
        mode = input(
            "Enter a letter to access the corresponding mode:\n"
            "\t- Press 'a' to add a new password\n"
            "\t- Press 'v' to view a password\n"
            "\t- Press 's' to view all sites you have stored\n"
            "\t- Press 'm' to modify an existing password\n"
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
        elif mode == 'q':
            'Quitting Program.'
            quit()
        else:
            print("mode not recognized.")


key = get_crypt_key()

db.connect_to_database()
db.confirm_tables_existence()
master_key.confirm_master_existence(key)
login.master_login(master_key.confirm_master_existence(key))

main_dialogue()
