import tkinter as tk
from tkinter import messagebox
import sqlite3
import joblib

# Load ML model
model = joblib.load("model.pkl")

# Database setup
conn = sqlite3.connect("banking.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT,
    password TEXT,
    balance REAL
)
""")

conn.commit()

# Main window
root = tk.Tk()
root.title("AI Banking App")
root.geometry("400x500")

# Variables
username_var = tk.StringVar()
password_var = tk.StringVar()

# Signup function
def signup():
    username = username_var.get()
    password = password_var.get()

    cursor.execute(
        "INSERT INTO users VALUES (?, ?, ?)",
        (username, password, 0)
    )
    conn.commit()

    messagebox.showinfo("Success", "Account created!")

# Login function
def login():
    username = username_var.get()
    password = password_var.get()

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )

    user = cursor.fetchone()

    if user:
        open_dashboard(username)
    else:
        messagebox.showerror("Error", "Invalid credentials")

# Dashboard
def open_dashboard(username):

    dashboard = tk.Toplevel(root)
    dashboard.title("Dashboard")
    dashboard.geometry("400x400")

    amount_var = tk.DoubleVar()

    def deposit():
        amount = amount_var.get()

        cursor.execute(
            "UPDATE users SET balance = balance + ? WHERE username=?",
            (amount, username)
        )

        conn.commit()

        messagebox.showinfo(
            "Success",
            f"Deposited ${amount}"
        )

    def withdraw():
        amount = amount_var.get()

        # AI Fraud Detection
        prediction = model.predict([[amount]])

        if prediction[0] == 1:
            messagebox.showwarning(
                "Fraud Alert",
                "Suspicious transaction detected!"
            )
            return

        cursor.execute(
            "UPDATE users SET balance = balance - ? WHERE username=?",
            (amount, username)
        )

        conn.commit()

        messagebox.showinfo(
            "Success",
            f"Withdrawn ${amount}"
        )

    def check_balance():
        cursor.execute(
            "SELECT balance FROM users WHERE username=?",
            (username,)
        )

        balance = cursor.fetchone()[0]

        messagebox.showinfo(
            "Balance",
            f"Current Balance: ${balance}"
        )

    tk.Label(dashboard, text="Amount").pack(pady=10)

    tk.Entry(
        dashboard,
        textvariable=amount_var
    ).pack()

    tk.Button(
        dashboard,
        text="Deposit",
        command=deposit
    ).pack(pady=10)

    tk.Button(
        dashboard,
        text="Withdraw",
        command=withdraw
    ).pack(pady=10)

    tk.Button(
        dashboard,
        text="Check Balance",
        command=check_balance
    ).pack(pady=10)

# UI
tk.Label(root, text="AI Banking App", font=("Arial", 20)).pack(pady=20)

tk.Label(root, text="Username").pack()
tk.Entry(root, textvariable=username_var).pack()

tk.Label(root, text="Password").pack()
tk.Entry(root, textvariable=password_var, show="*").pack()

tk.Button(root, text="Signup", command=signup).pack(pady=10)
tk.Button(root, text="Login", command=login).pack(pady=10)

root.mainloop()