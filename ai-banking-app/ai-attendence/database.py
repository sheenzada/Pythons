import sqlite3

class Database:

    def __init__(self):
        self.conn = sqlite3.connect("attendance.db")
        self.cursor = self.conn.cursor()

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            date TEXT,
            time TEXT
        )
        """)

        self.conn.commit()

    def insert_attendance(self, name, date, time):
        self.cursor.execute("""
        INSERT INTO attendance(name, date, time)
        VALUES (?, ?, ?)
        """, (name, date, time))

        self.conn.commit()

    def close(self):
        self.conn.close()