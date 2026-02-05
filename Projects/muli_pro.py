import tkinter as tk
from tkinter import ttk, messagebox

# Main window (ONLY ONE Tk)
win = tk.Tk()
win.title("User Form")
win.geometry("380x330")
win.resizable(False, False)

# Style
style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Custom.TButton",
    font=("Arial", 11, "bold"),
    padding=10
)

# Main Frame
main_frame = ttk.Frame(win, padding=25)
main_frame.pack(fill="both", expand=True)

# Title
ttk.Label(
    main_frame,
    text="User Information",
    font=("Arial", 16, "bold")
).grid(row=0, column=0, columnspan=2, pady=(0, 20))

# Variables
name_var = tk.StringVar()
email_var = tk.StringVar()
age_var = tk.StringVar()
gender_var = tk.StringVar(value="Male")
user_type = tk.StringVar(value="Student")

# Labels & Entries
labels = ["Name", "Email", "Age", "Gender", "User Type"]
for i, text in enumerate(labels):
    ttk.Label(main_frame, text=text + ":").grid(row=i+1, column=0, sticky="w", pady=6)

ttk.Entry(main_frame, textvariable=name_var, width=25).grid(row=1, column=1)
ttk.Entry(main_frame, textvariable=email_var, width=25).grid(row=2, column=1)
ttk.Entry(main_frame, textvariable=age_var, width=25).grid(row=3, column=1)

# Gender Combobox
gender_combo = ttk.Combobox(
    main_frame,
    textvariable=gender_var,
    values=("Male", "Female", "Other"),
    state="readonly",
    width=22
)
gender_combo.grid(row=4, column=1)

# Radio Buttons
radio_frame = ttk.Frame(main_frame)
radio_frame.grid(row=5, column=1, sticky="w")

ttk.Radiobutton(radio_frame, text="Student", variable=user_type, value="Student").pack(side="left", padx=5)
ttk.Radiobutton(radio_frame, text="Teacher", variable=user_type, value="Teacher").pack(side="left")

# Submit Function (NO new window)
def submit_action():
    if not name_var.get() or not email_var.get() or not age_var.get():
        messagebox.showwarning("Warning", "Please fill all fields!")
        return

    messagebox.showinfo(
        "Success",
        f"Name: {name_var.get()}\n"
        f"Email: {email_var.get()}\n"
        f"Age: {age_var.get()}\n"
        f"Gender: {gender_var.get()}\n"
        f"Type: {user_type.get()}"
    )

# Submit Button
submit_btn = ttk.Button(
    main_frame,
    text="Submit",
    style="Custom.TButton",
    command=submit_action
)
submit_btn.grid(row=6, column=0, columnspan=2, pady=20)

win.mainloop()
