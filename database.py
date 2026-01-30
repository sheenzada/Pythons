# import sqlite3

# class Database:
#     def __init__(self):
#         self.conn = sqlite3.connect("data/users.db")
#         self.cursor = self.conn.cursor()
#         self.cursor.execute("""
#             CREATE TABLE IF NOT EXISTS users (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 username TEXT UNIQUE,
#                 password TEXT,
#                 role TEXT DEFAULT 'User'
#             )
#         """)
#         self.conn.commit()

import sqlite3
import os

class Database:
    def __init__(self):
        # Ensure data folder exists
        if not os.path.exists("data"):
            os.makedirs("data")

        self.conn = sqlite3.connect("data/users.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT,
                role TEXT DEFAULT 'User'
            )
        """)
        self.conn.commit()




    def register_user(self, username, password):
        try:
            self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            self.conn.commit()
            return True
        except:
            return False

    def login_user(self, username, password):
        self.cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        return self.cursor.fetchone() is not None

    def get_all_users(self):
        self.cursor.execute("SELECT username, role FROM users")
        return self.cursor.fetchall()
