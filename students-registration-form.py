import tkinter as tk
from tkinter import messagebox, ttk
from database import Database

# Theme Colors
COLOR_DARK = "#212121"
COLOR_ACCENT = "#00adb5"
COLOR_LIGHT = "#eeeeee"

class SchoolApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Student Registry System Pro")
        self.geometry("1100x650")
        self.db = Database()
        self.current_user = "Admin" # Placeholder for demo

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.frames = {}
        for F in (StudentFormPage, ViewStudentsPage):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StudentFormPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        if hasattr(frame, "on_show"): frame.on_show()

# --- SIDEBAR COMPONENT ---
class Sidebar(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_DARK, width=200)
        self.pack_propagate(False)
        
        tk.Label(self, text="STUDENT OS", fg=COLOR_ACCENT, bg=COLOR_DARK, 
                 font=("Verdana", 14, "bold")).pack(pady=30)

        self.nav_btn("Register Student", lambda: controller.show_frame("StudentFormPage"))
        self.nav_btn("View Records", lambda: controller.show_frame("ViewStudentsPage"))
        self.nav_btn("Exit", self.quit)

    def nav_btn(self, text, command):
        btn = tk.Button(self, text=text, command=command, bg=COLOR_DARK, fg="white",
                        bd=0, font=("Arial", 11), pady=15, cursor="hand2", anchor="w", padx=20)
        btn.pack(fill="x")

# --- PAGE 1: REGISTRATION FORM ---
class StudentFormPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_LIGHT)
        self.controller = controller
        Sidebar(self, controller).pack(side="left", fill="y")

        content = tk.Frame(self, bg=COLOR_LIGHT, padx=50, pady=40)
        content.pack(side="right", fill="both", expand=True)

        tk.Label(content, text="Student Registration", font=("Arial", 24, "bold"), 
                 bg=COLOR_LIGHT, fg=COLOR_DARK).pack(anchor="w", pady=(0, 30))

        # Form Fields
        self.vars = {}
        for field in ["Student ID", "Full Name", "Email"]:
            tk.Label(content, text=field, bg=COLOR_LIGHT).pack(anchor="w")
            entry = tk.Entry(content, font=("Arial", 12), width=40)
            entry.pack(pady=(5, 15))
            self.vars[field] = entry

        tk.Label(content, text="Course", bg=COLOR_LIGHT).pack(anchor="w")
        self.course_box = ttk.Combobox(content, values=["Computer Science", "Business", "Arts", "Engineering"], width=38)
        self.course_box.pack(pady=(5, 20))

        tk.Button(content, text="SUBMIT REGISTRATION", bg=COLOR_ACCENT, fg="white", 
                  font=("Arial", 12, "bold"), padx=20, pady=10, command=self.save_data).pack(anchor="w")

    def save_data(self):
        s_id = self.vars["Student ID"].get()
        name = self.vars["Full Name"].get()
        email = self.vars["Email"].get()
        course = self.course_box.get()

        if s_id and name and course:
            if self.controller.db.add_student(s_id, name, email, course, "N/A"):
                messagebox.showinfo("Success", "Student Registered Successfully!")
                for e in self.vars.values(): e.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "ID already exists!")
        else:
            messagebox.showwarning("Warning", "Please fill all required fields")

# --- PAGE 2: DATA VIEW ---
class ViewStudentsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller
        Sidebar(self, controller).pack(side="left", fill="y")

        self.table_frame = tk.Frame(self, padx=20, pady=20)
        self.table_frame.pack(side="right", fill="both", expand=True)

        tk.Label(self.table_frame, text="Current Student Records", font=("Arial", 18, "bold")).pack(pady=10)

        # Scrollbar and Table
        scroll = tk.Scrollbar(self.table_frame)
        scroll.pack(side="right", fill="y")

        self.tree = ttk.Treeview(self.table_frame, columns=("ID", "Name", "Email", "Course"), 
                                 show="headings", yscrollcommand=scroll.set)
        for col in ("ID", "Name", "Email", "Course"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        
        self.tree.pack(fill="both", expand=True)
        scroll.config(command=self.tree.yview)

    def on_show(self):
        # Clear and reload data
        for i in self.tree.get_children(): self.tree.delete(i)
        for row in self.controller.db.get_all_students():
            self.tree.insert("", "end", values=row[:4])

if __name__ == "__main__":
    app = SchoolApp()
    app.mainloop()