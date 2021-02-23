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


key = get_crypt_key()

db.connect_to_database()
db.confirm_tables_existence()
master_key.confirm_master_existence(key)
login.master_login(master_key.confirm_master_existence(key))

# This works
# print("Let's create a new database entry (site, password)")
# dialogue.create_entry(key)

# Next, let's allow the user to retrieve password from database
# we need: entry_exists, read_one_entry
dialogue.view_one_entry(key)










