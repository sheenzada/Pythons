import tkinter as tk
from tkinter import messagebox, ttk
from database import Database

# Constants for Styling
BG_COLOR = "#2C3E50"
ACCENT_COLOR = "#3498DB"
TEXT_COLOR = "#ECF0F1"

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Enterprise User Management v2.0")
        self.geometry("800x550")
        self.db = Database()
        
        self.current_user = None

        # Main Container
        self.container = tk.Frame(self, bg=BG_COLOR)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (LoginFrame, RegisterFrame, DashboardFrame):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginFrame")

    def show_frame(self, page_name):
        # Security Guard: Prevent Dashboard access if not logged in
        if page_name == "DashboardFrame" and not self.current_user:
            messagebox.showwarning("Access Denied", "Please login first!")
            return
            
        frame = self.frames[page_name]
        frame.tkraise()
        if hasattr(frame, "on_show"):
            frame.on_show()

# ================== UI FRAMES ==================

class LoginFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_COLOR)
        self.controller = controller

        center_frame = tk.Frame(self, bg=BG_COLOR)
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(center_frame, text="MEMBER LOGIN", font=("Helvetica", 24, "bold"), fg=ACCENT_COLOR, bg=BG_COLOR).pack(pady=20)
        
        self.user_entry = self.create_input(center_frame, "Username")
        self.pass_entry = self.create_input(center_frame, "Password", show="*")

        tk.Button(center_frame, text="LOGIN", font=("Helvetica", 12, "bold"), bg=ACCENT_COLOR, fg="white", 
                  width=20, command=self.handle_login).pack(pady=20)
        
        tk.Button(center_frame, text="Create Account", fg=ACCENT_COLOR, bg=BG_COLOR, bd=0, 
                  command=lambda: controller.show_frame("RegisterFrame")).pack()

    def create_input(self, parent, label_text, show=None):
        tk.Label(parent, text=label_text, fg=TEXT_COLOR, bg=BG_COLOR).pack(anchor="w")
        entry = tk.Entry(parent, font=("Helvetica", 12), width=30, show=show)
        entry.pack(pady=5)
        return entry

    def handle_login(self):
        user = self.user_entry.get()
        pw = self.pass_entry.get()
        result = self.controller.db.login_user(user, pw)
        
        if result:
            self.controller.current_user = user
            self.controller.show_frame("DashboardFrame")
        else:
            messagebox.showerror("Error", "Invalid Credentials")

class DashboardFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#F4F7F6")
        self.controller = controller
        
        # Sidebar
        self.sidebar = tk.Frame(self, bg="#1A252F", width=200)
        self.sidebar.pack(side="left", fill="y")
        
        tk.Label(self.sidebar, text="ADMIN PANEL", fg="white", bg="#1A252F", font=("Helvetica", 12, "bold")).pack(pady=20)
        
        tk.Button(self.sidebar, text="Refresh List", command=self.load_data).pack(fill="x", padx=10, pady=5)
        tk.Button(self.sidebar, text="Logout", command=self.logout).pack(side="bottom", fill="x", padx=10, pady=20)

        # Main Content
        self.main_area = tk.Frame(self, bg="#F4F7F6")
        self.main_area.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        self.welcome_lbl = tk.Label(self.main_area, text="", font=("Helvetica", 18), bg="#F4F7F6")
        self.welcome_lbl.pack(anchor="w")

        # Table for Users
        self.tree = ttk.Treeview(self.main_area, columns=("Username", "Role"), show="headings")
        self.tree.heading("Username", text="Username")
        self.tree.heading("Role", text="Role")
        self.tree.pack(fill="both", expand=True, pady=20)

    def on_show(self):
        self.welcome_lbl.config(text=f"Welcome, {self.controller.current_user}")
        self.load_data()

    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for user in self.controller.db.get_all_users():
            self.tree.insert("", tk.END, values=user)

    def logout(self):
        self.controller.current_user = None
        self.controller.show_frame("LoginFrame")

class RegisterFrame(tk.Frame):
    # (Similar structure to LoginFrame, calling self.controller.db.register_user)
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_COLOR)
        self.controller = controller
        tk.Label(self, text="Register Page", font=("Helvetica", 20), fg="white", bg=BG_COLOR).pack(pady=50)
        tk.Button(self, text="Back to Login", command=lambda: controller.show_frame("LoginFrame")).pack()

if __name__ == "__main__":
    app = App()
    app.mainloop()