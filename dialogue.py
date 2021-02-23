"""Contains the dialogue for user-database interaction"""

import db
import crypt_utils


def create_entry(key):
    """User creates a site and password to be stored in database"""

    new_site = input("\nCreating a new entry.\n"
                     "Please type the name of the site for your new password (ex. 'youtube'): ")
    new_pass = input(f"\nPlease type your new password for {new_site}: ")

    pass_confirm = input(f"\nFor confirmation, type your new password for {new_site} again: ")
    if new_pass == pass_confirm:

        print(f"\nReady to insert new entry for site '{new_site}' with password: {new_pass}")
        confirm_new_entry = input("\nType 'confirm' to proceed if this is correct. ('q' to quit): ")

        if confirm_new_entry == 'confirm':

            encrypted_pass = crypt_utils.encrypt_password(new_pass.encode('UTF-8'), key)
            db.insert_entry(new_site, encrypted_pass)
            print("\nNew entry successful!\n")

        elif confirm_new_entry == 'q':
            print("Quitting operation. No changes were made.\n")
            pass

        else:
            print("Command not recognized.\n")

    else:
        print("Passwords did not match. No changes were made.")
