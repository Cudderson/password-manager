"""File that handles the creation of the master key, as well as retrieving it"""


def create_master_key():
    """Creates and returns master password"""

    master_key_query = 'INSERT INTO Master (master_key) VALUES (%s)'

    print("\nBefore we begin, let's set a master password for this program.\n"
          "Your master password will be required to access your stored passwords.")

    new_master = input("\nEnter your new master password: ")
    new_master_confirm = input("To confirm, enter your new master password again: ")

    if new_master == new_master_confirm:

        store_new_master_confirm = input(f"\nStore new master password '{new_master}' ? (yes/no): ")

        if store_new_master_confirm == 'yes':

            return new_master, master_key_query

        elif store_new_master_confirm == 'no':

            print("\nNew master password was not created. To use Password Manager, you must create one.")
            return create_master_key()

        else:
            print("\nCommand not recognized. No changes were made.")
            return create_master_key()
    else:
        print("\nPasswords did not match. Nothing was altered.")
        return create_master_key()
