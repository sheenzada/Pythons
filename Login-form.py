from flask import Flask, render_template_string, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = "secretkey"

# ================= DATABASE =================

def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        email TEXT,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# ================= HOME =================

@app.route("/")
def home():
    if "user" in session:
        return redirect("/dashboard")

    return render_template_string("""

    <html>
    <head>
        <title>Login System</title>

        <style>
            body{
                font-family: Arial;
                background: linear-gradient(to right,#4facfe,#00f2fe);
                text-align:center;
                padding-top:100px;
            }

            .box{
                width:400px;
                background:white;
                margin:auto;
                padding:30px;
                border-radius:10px;
                box-shadow:0px 0px 15px gray;
            }

            a{
                text-decoration:none;
                background:blue;
                color:white;
                padding:12px 20px;
                border-radius:5px;
                display:inline-block;
                margin:10px;
            }
        </style>

    </head>

    <body>

        <div class="box">

            <h1>Python Login System</h1>

            <a href="/register">Register</a>
            <a href="/login">Login</a>

        </div>

    </body>
    </html>

    """)

# ================= REGISTER =================

@app.route("/register", methods=["GET","POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])

        try:
            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()

            cursor.execute("""
            INSERT INTO users(username,email,password)
            VALUES(?,?,?)
            """,(username,email,password))

            conn.commit()
            conn.close()

            return redirect("/login")

        except:
            return "Username already exists!"

    return render_template_string("""

    <html>
    <head>

        <title>Register</title>

        <style>

            body{
                font-family:Arial;
                background:#f2f2f2;
            }

            .form-box{
                width:450px;
                background:white;
                margin:auto;
                margin-top:50px;
                padding:30px;
                border-radius:10px;
                box-shadow:0px 0px 10px gray;
            }

            input{
                width:100%;
                padding:12px;
                margin-top:10px;
                margin-bottom:20px;
            }

            button{
                width:100%;
                padding:12px;
                background:green;
                color:white;
                border:none;
                font-size:18px;
            }

        </style>

    </head>

    <body>

        <div class="form-box">

            <h2>Create Account</h2>

            <form method="POST">

                <input type="text" name="username" placeholder="Username" required>

                <input type="email" name="email" placeholder="Email" required>

                <input type="password" name="password" placeholder="Password" required>

                <button type="submit">Register</button>

            </form>

        </div>

    </body>
    </html>

    """)

# ================= LOGIN =================

@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username=?",(username,))
        user = cursor.fetchone()

        conn.close()

        if user and check_password_hash(user[3], password):

            session["user"] = username
            return redirect("/dashboard")

        else:
            return "Invalid Username or Password"

    return render_template_string("""

    <html>
    <head>

        <title>Login</title>

        <style>

            body{
                font-family:Arial;
                background:linear-gradient(to right,#8360c3,#2ebf91);
            }

            .login-box{
                width:400px;
                background:white;
                margin:auto;
                margin-top:100px;
                padding:30px;
                border-radius:10px;
                box-shadow:0px 0px 15px black;
            }

            input{
                width:100%;
                padding:12px;
                margin-top:10px;
                margin-bottom:20px;
            }

            button{
                width:100%;
                padding:12px;
                background:blue;
                color:white;
                border:none;
                font-size:18px;
            }

        </style>

    </head>

    <body>

        <div class="login-box">

            <h2>User Login</h2>

            <form method="POST">

                <input type="text" name="username" placeholder="Username" required>

                <input type="password" name="password" placeholder="Password" required>

                <button type="submit">Login</button>

            </form>

        </div>

    </body>
    </html>

    """)

# ================= DASHBOARD =================

@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/login")

    return render_template_string("""

    <html>

    <head>

        <title>Dashboard</title>

        <style>

            body{
                font-family:Arial;
                background:#e3f2fd;
                text-align:center;
                padding-top:100px;
            }

            .dashboard{
                width:500px;
                background:white;
                margin:auto;
                padding:40px;
                border-radius:10px;
                box-shadow:0px 0px 15px gray;
            }

            a{
                text-decoration:none;
                background:red;
                color:white;
                padding:12px 20px;
                border-radius:5px;
            }

        </style>

    </head>

    <body>

        <div class="dashboard">

            <h1>Welcome {{user}}</h1>

            <p>Login Successful</p>

            <a href="/logout">Logout</a>

        </div>

    </body>

    </html>

    """, user=session["user"])

# ================= LOGOUT =================

@app.route("/logout")
def logout():

    session.pop("user", None)

    return redirect("/login")

# ================= RUN =================

if __name__ == "__main__":
    app.run(debug=True)