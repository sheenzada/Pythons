import sqlite3
import hashlib

class Database:
    def __init__(self, db_name="system.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT,
                role TEXT DEFAULT 'User'
            )
        """)
        self.conn.commit()

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, username, password):
        try:
            hashed = self.hash_password(password)
            self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed))
            self.conn.commit()
            return True, "Registration Successful"
        except sqlite3.IntegrityError:
            return False, "Username already exists"

    def login_user(self, username, password):
        hashed = self.hash_password(password)
        self.cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashed))
        return self.cursor.fetchone()

    def get_all_users(self):
        self.cursor.execute("SELECT username, role FROM users")
        return self.cursor.fetchall()