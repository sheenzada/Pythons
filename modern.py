import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import hashlib

# ================= DATABASE LAYER =================
class Database:
    def __init__(self):
        self.conn = sqlite3.connect("enterprise.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT,
                role TEXT
            )
        """)
        self.conn.commit()

    def hash_pw(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def register(self, user, pw):
        try:
            self.cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                                (user, self.hash_pw(pw), "User"))
            self.conn.commit()
            return True
        except: return False

    def login(self, user, pw):
        self.cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (user, self.hash_pw(pw)))
        return self.cursor.fetchone()

# ================= UI COMPONENTS =================
class ModernButton(tk.Button):
    """A custom button that changes color on hover"""
    def __init__(self, master, **kwargs):
        super().__init__(master, font=("Segoe UI", 10, "bold"), cursor="hand2", bd=0, padx=20, pady=10, **kwargs)
        self.default_bg = kwargs.get("bg", "#34495e")
        self.hover_bg = "#2c3e50"
        self.bind("<Enter>", lambda e: self.config(bg=self.hover_bg))
        self.bind("<Leave>", lambda e: self.config(bg=self.default_bg))

# ================= MAIN APPLICATION =================
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Titan OS - Management System")
        self.geometry("1000x600")
        self.db = Database()
        self.current_user = None

        # Main Container
        self.main_container = tk.Frame(self, bg="#ecf0f1")
        self.main_container.pack(fill="both", expand=True)

        self.frames = {}
        for F in (LoginFrame, RegisterFrame, DashboardFrame):
            frame = F(self.main_container, self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)

        self.show_frame("LoginFrame")

    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()
        if hasattr(frame, "refresh"): frame.refresh()

# ================= PAGES =================
class LoginFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#2c3e50")
        self.controller = controller

        center_card = tk.Frame(self, bg="white", padx=50, pady=50)
        center_card.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(center_card, text="System Login", font=("Segoe UI", 22, "bold"), bg="white", fg="#2c3e50").pack(pady=20)
        
        self.user = self.entry_factory(center_card, "Username")
        self.pw = self.entry_factory(center_card, "Password", show="*")

        ModernButton(center_card, text="LOGIN", bg="#3498db", fg="white", 
                     command=self.attempt_login).pack(fill="x", pady=20)
        
        tk.Button(center_card, text="Create new account", fg="#3498db", bg="white", bd=0, 
                  command=lambda: controller.show_frame("RegisterFrame")).pack()

    def entry_factory(self, parent, label, show=None):
        tk.Label(parent, text=label, bg="white", font=("Segoe UI", 9)).pack(anchor="w")
        e = tk.Entry(parent, font=("Segoe UI", 12), width=30, bg="#f9f9f9", bd=1)
        if show: e.config(show=show)
        e.pack(pady=(5, 15))
        return e

    def attempt_login(self):
        res = self.controller.db.login(self.user.get(), self.pw.get())
        if res:
            self.controller.current_user = self.user.get()
            self.controller.show_frame("DashboardFrame")
        else:
            messagebox.showerror("Error", "Access Denied")

class RegisterFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#2c3e50")
        self.controller = controller
        # [Simplified for space - similar to LoginFrame structure]
        tk.Label(self, text="Register New User", fg="white", bg="#2c3e50", font=("Arial", 20)).pack(pady=50)
        ModernButton(self, text="Back", bg="#95a5a6", fg="white", command=lambda: controller.show_frame("LoginFrame")).pack()

class DashboardFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f5f6fa")
        self.controller = controller

        # Sidebar
        self.sidebar = tk.Frame(self, bg="#2f3640", width=250)
        self.sidebar.pack(side="left", fill="y")

        tk.Label(self.sidebar, text="TITAN OS", font=("Segoe UI", 18, "bold"), bg="#2f3640", fg="white").pack(pady=30)
        
        ModernButton(self.sidebar, text="Overview", bg="#2f3640", fg="white", width=20).pack(pady=5)
        ModernButton(self.sidebar, text="Users", bg="#2f3640", fg="white", width=20).pack(pady=5)
        ModernButton(self.sidebar, text="Logout", bg="#e74c3c", fg="white", width=20, 
                     command=lambda: controller.show_frame("LoginFrame")).pack(side="bottom", pady=20)

        # Main Area
        self.content = tk.Frame(self, bg="#f5f6fa", padx=30, pady=30)
        self.content.pack(side="right", fill="both", expand=True)

        self.header = tk.Label(self.content, text="", font=("Segoe UI", 24), bg="#f5f6fa")
        self.header.pack(anchor="nw")

    def refresh(self):
        self.header.config(text=f"Welcome, {self.controller.current_user}")

if __name__ == "__main__":
    app = App()
    app.mainloop()