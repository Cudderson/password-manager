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