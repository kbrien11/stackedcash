import sqlite3
import os

DIR = os.path.dirname(__file__)
DBNAME = "stacked.db"
DBPATH = os.path.join(DIR, DBNAME)



def schema(dbpath):
    with sqlite3.connect(dbpath) as connection:
        cursor = connection.cursor()

        cursor.execute("DROP TABLE IF EXISTS users;")

        SQL = """CREATE TABLE users (
                pk INTEGER PRIMARY KEY AUTOINCREMENT,
                email VARCHAR(128),
                password_hash VARCHAR(32),
                first_name VARCHAR(32),
                last_name VARCHAR(32),
                company varchar(64),
                position VARCHAR(20),
                city VARCHAR(32),
                salary FLOAT,
                api_key VARCHAR(15)
            );"""

        cursor.execute(SQL)


        cursor.execute("DROP TABLE IF EXISTS jobs;")

        SQL = """CREATE TABLE jobs (
                pk INTEGER PRIMARY KEY AUTOINCREMENT,
                department VARCHAR(30),
                level VARCHAR(20),
                years INTEGER,
                happy INTEGER,
                company VARCHAR(30),
                users_pk INTEGER,
                FOREIGN KEY(users_pk) REFERENCES users(pk),
                FOREIGN KEY(company) REFERENCES users(company)
                
            );"""

        cursor.execute(SQL)


        cursor.execute("DROP TABLE IF EXISTS reviews;")
        

        SQL = """CREATE TABLE reviews(
             pk INTEGER PRIMARY KEY AUTOINCREMENT,
             review TEXT,
             company VARCHAR(30),
             time_stamp VARCHAR(30),
             pros TEXT,
             cons TEXT,
             users_pk INTEGER,
             FOREIGN KEY(company) REFERENCES users(company),
             FOREIGN KEY(users_pk) REFERENCES users(pk)

            );"""

        cursor.execute("DROP TABLE IF EXISTS bookings;")
        

        SQL = """CREATE TABLE bookings(
             pk INTEGER PRIMARY KEY AUTOINCREMENT,
             first_name VARCHAR(20),
             date_stamp VARCHAR(30),
             time_stamp VARCHAR(30),
             full_date VARCHAR(30),
             users_pk INTEGER,
             FOREIGN KEY(first_name) REFERENCES users(first_name),
             FOREIGN KEY(users_pk) REFERENCES users(pk)

            );"""


        cursor.execute(SQL)


if __name__ == "__main__":
    schema("stacked.db")
