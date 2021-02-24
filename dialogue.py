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


def view_one_entry(key):
    site_to_find = input("\nPlease enter the site name for the password you need. (twitter): ")
    entry_to_view = db.entry_exists(site_to_find)

    if entry_to_view is not None:

        desired_pass = db.get_one_entry(site_to_find)
        desired_pass = desired_pass[1]
        print(f"\nHere is your encrypted password for {site_to_find}:\n{desired_pass}")
        confirm_decrypt = input("\nType 'decrypt' to view your password: ")

        if confirm_decrypt == 'decrypt':

            desired_pass = desired_pass.encode("UTF-8")
            password = crypt_utils.decrypt_password(desired_pass, key)
            print(f"\nYour password for {site_to_find} is: {password.decode()}")
            input("\nPress enter to continue: ")

        else:
            print("\nCommand not recognized. No changes were made.\n")

    else:
        print(f"\nCould not find entry with site name '{site_to_find}'")
        print(f"Cancelling operation. Nothing was altered.\n")


def modify_password(key):
    site_to_modify = input("\nPlease enter the site name for the password you are modifying: ")
    # make sure site name exists in db:
    found_entry = db.entry_exists(site_to_modify)

    if found_entry is not None:

        found_site = found_entry[0]
        found_pass = found_entry[1]

        print(f"\nReady to change password for {found_site}")

        # decrypt current password
        decrypted_password = crypt_utils.decrypt_password(found_pass.encode("UTF-8"), key)

        print(f"\nCurrent password for {found_site} is {decrypted_password.decode()}")
        modded_pass = input(f"\nEnter your new password for {found_site}: ")
        confirm_modded_pass = input(f"Confirm new password for {found_site}: ")

        if modded_pass == confirm_modded_pass:

            new_password = crypt_utils.encrypt_password(modded_pass.encode("UTF-8"), key)
            db.modify_one_password(found_site, new_password)

            print(f"\nNew entry added successfully!"
                  f"\nYour new password for {found_site} is '{modded_pass}'\n")

        else:
            print("\nNew passwords did not match. No changes were made.\n")

    else:
        print(f"Could not find site '{site_to_modify}' in database.")


def dialogue_delete_entry():
    """Dialogue for deleting an entry from database"""

    site_to_delete = input("\nEnter the name of the site that you'd like to delete its entry for: ")

    site_entry_id = db.get_entry_id(site_to_delete)

    if site_entry_id is not None:

        db.delete_entry_from_db(site_entry_id)

    else:
        pass
