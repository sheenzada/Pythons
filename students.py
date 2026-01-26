import sqlite3
import hashlib

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("school_data.db")
        self.cursor = self.conn.cursor()
        self.setup_tables()

    def setup_tables(self):
        # Users table for Login
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE, password TEXT
            )""")
        # Students table for Data Entry
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id TEXT PRIMARY KEY,
                name TEXT, email TEXT, course TEXT, gender TEXT
            )""")
        self.conn.commit()

    def add_student(self, s_id, name, email, course, gender):
        try:
            self.cursor.execute("INSERT INTO students VALUES (?, ?, ?, ?, ?)", 
                                (s_id, name, email, course, gender))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def get_all_students(self):
        self.cursor.execute("SELECT * FROM students")
        return self.cursor.fetchall()