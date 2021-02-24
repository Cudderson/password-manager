"""This file will handle SQL database setup, also contains functions for reading/writing to database"""

import mysql.connector
import crypt_key
import time

# Retrieve password for database connection
with open('password.txt', 'r') as f:
    password = f.readline()


def connect_to_database():
    db = mysql.connector.connect(
        host='localhost',
        username='root',
        password=password,
        database='pm_db',
    )

    return db


pm_db = connect_to_database()

# Cursor for interacting with database
cursor = pm_db.cursor()


def create_site_table():
    """Returns the query needed to create the table for sites in database"""

    create_site_table_query = \
        'CREATE TABLE Sites (entryID int AUTO_INCREMENT, ' \
        'Site VARCHAR(100) NOT NULL, ' \
        'PRIMARY KEY (entryID))'

    return create_site_table_query


def create_pass_table():
    """Returns the query needed to create the table for passwords in database"""

    create_pass_table_query = \
        'CREATE TABLE Passwords ' \
        '(entryID int AUTO_INCREMENT, ' \
        'Passwords BINARY(100) NOT NULL, ' \
        'FOREIGN KEY (entryID) REFERENCES Sites(entryID))'

    return create_pass_table_query


def create_master_table():
    """Returns the query needed to create the table for the master key in database"""

    create_master_table_query = \
        'CREATE TABLE Master ' \
        '(master_key_id int AUTO_INCREMENT, ' \
        'master_key BINARY(100) NOT NULL, ' \
        'PRIMARY KEY (master_key_id))'

    return create_master_table_query


def create_tables():
    """Executes all queries needed for db schema setup"""

    create_site_table_query = create_site_table()
    create_pass_table_query = create_pass_table()
    create_master_table_query = create_master_table()

    cursor.execute(create_site_table_query)
    cursor.execute(create_pass_table_query)
    cursor.execute(create_master_table_query)

    pm_db.commit()


def tables_exist():
    """Checks if db schema is set up properly and returns a boolean"""

    tables_in_db = False
    tables_exist_query = 'SHOW TABLES'
    cursor.execute(tables_exist_query)
    my_tables = cursor.fetchall()

    if len(my_tables) == 3:
        tables_in_db = True

    return tables_in_db


def store_encryption_key():
    """Stores a newly generated key in a bytes file"""

    # create crypt key
    new_crypt_key = crypt_key.create_crypt_key()

    with open('crypt_key.txt', "wb") as f:
        f.write(new_crypt_key)


def confirm_tables_existence():
    """Ensures user's database has proper schema for using program"""

    if tables_exist():
        print("Database found.")
    else:
        create_tables()
        print("Database Schema created successfully...")
        time.sleep(2)
        store_encryption_key()
        print("Encryption Key created and stored successfully...")
        time.sleep(2)


def insert_entry(new_site_name, new_password):
    """Adds a single entry to mysql database (site, password)"""

    insert_query_site = 'INSERT INTO Sites (Site) VALUES (%s)'
    insert_query_pass = 'INSERT INTO Passwords (Passwords) VALUES (%s)'
    cursor.execute(insert_query_site, (new_site_name,))
    pm_db.commit()
    cursor.execute(insert_query_pass, (new_password,))
    pm_db.commit()


def entry_exists(site):
    """Makes sure that a given entry exists in database before handling"""

    entry_exists_query = "SELECT sites.site, passwords.passwords " \
                         "FROM Sites, Passwords " \
                         "WHERE sites.site = (%s) " \
                         "AND sites.entryid = passwords.entryid"

    cursor.execute(entry_exists_query, (site,))
    existing_entry = cursor.fetchone()
    return existing_entry


def get_one_entry(site_to_match):
    """Returns the password for a user-specified site"""

    get_one_query = 'SELECT sites.site, passwords.passwords ' \
                    'FROM sites, passwords ' \
                    'WHERE sites.entryid = passwords.entryid ' \
                    'AND sites.site = (%s) '

    cursor.execute(get_one_query, (site_to_match,))
    one_entry = cursor.fetchone()
    return one_entry


def read_all_entries():
    """Displays all database information, in the form: (entryid, site, password)"""

    read_all_query = 'SELECT sites.entryid, sites.site, passwords.passwords ' \
                     'FROM sites, passwords ' \
                     'WHERE sites.entryid = passwords.entryid'

    cursor.execute(read_all_query)
    all_entries = cursor.fetchall()

    print("\n")
    for entry in all_entries:
        print(entry)

    input("\nPress enter to continue:")


def modify_one_password(site_to_mod, pass_to_mod):
    """Updates/Modifies the password for a user-given site"""

    modify_pass_query = 'UPDATE Passwords, Sites ' \
                        'SET passwords = (%s) ' \
                        'WHERE sites.site = (%s) ' \
                        'AND sites.entryid = passwords.entryid'

    cursor.execute(modify_pass_query, (pass_to_mod, site_to_mod))
    pm_db.commit()


def get_entry_id(site_to_match):
    """Returns the entry_id for a given site in database table"""

    entry_id_query = 'SELECT sites.entryid ' \
                     'FROM Sites ' \
                     'WHERE sites.site = (%s)'

    cursor.execute(entry_id_query, (site_to_match,))
    entry_id = cursor.fetchone()
    if entry_id:

        confirmation = input(f"\nYou are about to delete your password for site '{site_to_match}'.\n"
                             f"Type 'confirm' to continue, or 'q' to quit: ")

        if confirmation == 'confirm':
            return entry_id[0]
        elif confirmation == 'q':
            print("\nCancelling Operation. Nothing was altered.")
            pass
        else:
            print("\nCouldn't recognize command. Cancelling the operation. Nothing was deleted.")
            pass

    else:
        print(f"\nCouldn't find site with name '{site_to_match}'. Nothing was altered.\n")


def delete_entry_from_db(entry_id):
    """Deletes a site & password from database"""

    delete_site_query = 'DELETE FROM sites ' \
                        'WHERE sites.entryid = (%s) '

    delete_pass_query = 'DELETE FROM passwords ' \
                        'WHERE passwords.entryid = (%s) '

    cursor.execute(delete_pass_query, (entry_id,))
    pm_db.commit()

    cursor.execute(delete_site_query, (entry_id,))
    pm_db.commit()

    print(f"\nDeleted entry successfully.")
