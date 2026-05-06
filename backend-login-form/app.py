import os
import sqlite3
from flask import Flask, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# 🔐 Secret Key
app.config['SECRET_KEY'] = 'super-secret-key-change-this'

# 📁 Database Setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'users.db')


# ---------------------------
# Database Helper
# ---------------------------
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# ---------------------------
# Initialize Database
# ---------------------------
def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()


init_db()


# ---------------------------
# Home Route (Fixes 404)
# ---------------------------
@app.route('/')
def home():
    return jsonify({
        "status": "API running ✅",
        "endpoints": {
            "POST /register": "Create user",
            "POST /login": "Login user",
            "GET /dashboard": "Protected route",
            "POST /logout": "Logout user"
        }
    })


# ---------------------------
# Register
# ---------------------------
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if not data:
        return jsonify({"error": "JSON data required"}), 400

    username = data.get('username')
    password = data.get('password')

    # ✅ Validation
    if not username or not password:
        return jsonify({"error": "Username & password required"}), 400

    if len(password) < 4:
        return jsonify({"error": "Password must be at least 4 characters"}), 400

    hashed_password = generate_password_hash(password)

    try:
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hashed_password)
        )

        conn.commit()
        conn.close()

        return jsonify({"message": "User registered successfully"}), 201

    except sqlite3.IntegrityError:
        return jsonify({"error": "Username already exists"}), 409

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------------------------
# Login
# ---------------------------
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data:
        return jsonify({"error": "JSON data required"}), 400

    username = data.get('username')
    password = data.get('password')

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()

    conn.close()

    if user and check_password_hash(user['password'], password):
        session['user_id'] = user['id']
        session['username'] = user['username']

        return jsonify({
            "message": "Login successful",
            "user": user['username']
        })

    return jsonify({"error": "Invalid credentials"}), 401


# ---------------------------
# Protected Route
# ---------------------------
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    return jsonify({
        "message": f"Welcome {session['username']} 🎉"
    })


# ---------------------------
# Logout
# ---------------------------
@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully"})


# ---------------------------
# Run App
# ---------------------------
if __name__ == '__main__':
    print("Database path:", DB_PATH)
    app.run(debug=True)