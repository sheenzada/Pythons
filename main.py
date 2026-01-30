import tkinter as tk
from tkinter import messagebox, ttk
from database import Database

# ----------------- STYLING -----------------
BG_COLOR = "#2C3E50"
ACCENT_COLOR = "#3498DB"
TEXT_COLOR = "#ECF0F1"
DASH_BG = "#F4F7F6"
SIDEBAR_BG = "#1A252F"

# ----------------- MAIN APP -----------------
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Enterprise User Management v3.0")
        self.geometry("900x600")
        self.db = Database()
        self.current_user = None

        # Container
        self.container = tk.Frame(self, bg=BG_COLOR)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Frames
        self.frames = {}
        for F in (LoginFrame, RegisterFrame, DashboardFrame, AddUserFrame):
            frame = F(parent=self.container, controller=self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginFrame")

    def show_frame(self, page_name):
        if page_name == "DashboardFrame" and not self.current_user:
            messagebox.showwarning("Access Denied", "Please login first!")
            return
        frame = self.frames[page_name]
        frame.tkraise()
        if hasattr(frame, "on_show"):
            frame.on_show()

# ----------------- LOGIN FRAME -----------------
class LoginFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_COLOR)
        self.controller = controller

        center_frame = tk.Frame(self, bg=BG_COLOR)
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(center_frame, text="MEMBER LOGIN", font=("Helvetica", 26, "bold"),
                 fg=ACCENT_COLOR, bg=BG_COLOR).pack(pady=20)

        self.user_entry = self.create_input(center_frame, "Username")
        self.pass_entry = self.create_input(center_frame, "Password", show="*")

        tk.Button(center_frame, text="LOGIN", font=("Helvetica", 14, "bold"),
                  bg=ACCENT_COLOR, fg="white", width=25, command=self.handle_login).pack(pady=15)

        tk.Button(center_frame, text="Create Account", fg=ACCENT_COLOR, bg=BG_COLOR, bd=0,
                  command=lambda: controller.show_frame("RegisterFrame")).pack(pady=5)

    def create_input(self, parent, label, show=None):
        tk.Label(parent, text=label, fg=TEXT_COLOR, bg=BG_COLOR, anchor="w").pack(fill="x")
        entry = tk.Entry(parent, font=("Helvetica", 12), show=show)
        entry.pack(pady=5)
        return entry

    def handle_login(self):
        user = self.user_entry.get().strip()
        pw = self.pass_entry.get().strip()
        if self.controller.db.login_user(user, pw):
            self.controller.current_user = user
            self.controller.show_frame("DashboardFrame")
        else:
            messagebox.showerror("Error", "Invalid Credentials")

# ----------------- REGISTER FRAME -----------------
class RegisterFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_COLOR)
        self.controller = controller

        frame = tk.Frame(self, bg=BG_COLOR)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame, text="REGISTER", font=("Helvetica", 26, "bold"),
                 fg=ACCENT_COLOR, bg=BG_COLOR).pack(pady=20)

        self.user_entry = self.create_input(frame, "Username")
        self.pass_entry = self.create_input(frame, "Password", show="*")

        tk.Button(frame, text="REGISTER", font=("Helvetica", 14, "bold"),
                  bg=ACCENT_COLOR, fg="white", width=25, command=self.handle_register).pack(pady=15)

        tk.Button(frame, text="Back to Login", fg=ACCENT_COLOR, bg=BG_COLOR, bd=0,
                  command=lambda: controller.show_frame("LoginFrame")).pack(pady=5)

    def create_input(self, parent, label, show=None):
        tk.Label(parent, text=label, fg=TEXT_COLOR, bg=BG_COLOR, anchor="w").pack(fill="x")
        entry = tk.Entry(parent, font=("Helvetica", 12), show=show)
        entry.pack(pady=5)
        return entry

    def handle_register(self):
        user = self.user_entry.get().strip()
        pw = self.pass_entry.get().strip()
        if self.controller.db.register_user(user, pw):
            messagebox.showinfo("Success", "Account created! Please login.")
            self.controller.show_frame("LoginFrame")
        else:
            messagebox.showerror("Error", "Username already exists.")

# ----------------- DASHBOARD -----------------
class DashboardFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=DASH_BG)
        self.controller = controller

        # Sidebar
        self.sidebar = tk.Frame(self, bg=SIDEBAR_BG, width=220)
        self.sidebar.pack(side="left", fill="y")
        tk.Label(self.sidebar, text="ADMIN PANEL", fg="white", bg=SIDEBAR_BG,
                 font=("Helvetica", 14, "bold")).pack(pady=20)
        tk.Button(self.sidebar, text="Add User", command=lambda: controller.show_frame("AddUserFrame")).pack(fill="x", padx=10, pady=5)
        tk.Button(self.sidebar, text="Refresh List", command=self.load_data).pack(fill="x", padx=10, pady=5)
        tk.Button(self.sidebar, text="Logout", command=self.logout).pack(side="bottom", fill="x", padx=10, pady=20)

        # Main Content
        self.main_area = tk.Frame(self, bg=DASH_BG)
        self.main_area.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        self.welcome_lbl = tk.Label(self.main_area, text="", font=("Helvetica", 18), bg=DASH_BG)
        self.welcome_lbl.pack(anchor="w")

        self.tree = ttk.Treeview(self.main_area, columns=("Username", "Role"), show="headings")
        self.tree.heading("Username", text="Username")
        self.tree.heading("Role", text="Role")
        self.tree.pack(fill="both", expand=True, pady=20)

    def on_show(self):
        self.welcome_lbl.config(text=f"Welcome, {self.controller.current_user}")
        self.load_data()

    def load_data(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for user in self.controller.db.get_all_users():
            self.tree.insert("", "end", values=user)

    def logout(self):
        self.controller.current_user = None
        self.controller.show_frame("LoginFrame")

# ----------------- ADD USER FRAME -----------------
class AddUserFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=DASH_BG)
        self.controller = controller

        tk.Label(self, text="Add New User", font=("Helvetica", 24, "bold"), bg=DASH_BG).pack(pady=30)

        self.user_entry = self.create_input("Username")
        self.pass_entry = self.create_input("Password", show="*")
        self.role_entry = self.create_input("Role (Admin/User)")

        tk.Button(self, text="Add User", font=("Helvetica", 14, "bold"),
                  bg=ACCENT_COLOR, fg="white", command=self.add_user).pack(pady=15)
        tk.Button(self, text="Back", bg=SIDEBAR_BG, fg="white",
                  command=lambda: controller.show_frame("DashboardFrame")).pack(pady=5)

    def create_input(self, label, show=None):
        tk.Label(self, text=label, bg=DASH_BG, font=("Helvetica", 12)).pack()
        entry = tk.Entry(self, font=("Helvetica", 12), show=show)
        entry.pack(pady=5)
        return entry

    def add_user(self):
        user = self.user_entry.get().strip()
        pw = self.pass_entry.get().strip()
        role = self.role_entry.get().strip() or "User"
        if self.controller.db.register_user(user, pw):
            messagebox.showinfo("Success", f"User '{user}' added!")
            self.controller.show_frame("DashboardFrame")
        else:
            messagebox.showerror("Error", "Username already exists!")

# ----------------- RUN APP -----------------
if __name__ == "__main__":
    app = App()
    app.mainloop()
