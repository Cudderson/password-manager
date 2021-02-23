"""Conatins the functionality for logging into the program and accessing database"""


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
        return master_login(master_from_db)