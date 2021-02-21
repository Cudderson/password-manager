"""This file will handle SQL database setup"""

import mysql.connector

with open('password.txt', 'r') as f:
    password = f.readline()

pm_db = mysql.connector.connect(
    host='localhost',
    username='root',
    password=password,
    database='pm_db',
)

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


def create_key_table():
    """Returns the query needed to create the table for encryption key in database"""

    create_key_table_query = \
        'CREATE TABLE Crypt ' \
        '(key_id int AUTO_INCREMENT, ' \
        'crypt_key BINARY(120) NOT NULL, ' \
        'PRIMARY KEY (key_id))'

    return create_key_table_query


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
    create_key_table_query = create_key_table()
    create_master_table_query = create_master_table()

    cursor.execute(create_site_table_query)
    cursor.execute(create_pass_table_query)
    cursor.execute(create_master_table_query)
    cursor.execute(create_key_table_query)

    pm_db.commit()


create_tables()
