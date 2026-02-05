import tkinter as tk
from tkinter import ttk

# Main window
win = tk.Tk()
win.title("User Form")
win.geometry("350x300")
win.resizable(False, False)

# Style
style = ttk.Style()
style.theme_use("clam")

# Main frame (for clean layout)
main_frame = ttk.Frame(win, padding=20)
main_frame.grid(row=0, column=0, sticky="W")

# Title
title_label = ttk.Label(
    main_frame,
    text="User Information",
    font=("Arial", 14, "bold")
)
title_label.grid(row=0, column=0, columnspan=2, pady=(0, 15))

# Labels
ttk.Label(main_frame, text="Name:").grid(row=1, column=0, sticky=tk.W, pady=5)
ttk.Label(main_frame, text="Email:").grid(row=2, column=0, sticky=tk.W, pady=5)
ttk.Label(main_frame, text="Age:").grid(row=3, column=0, sticky=tk.W, pady=5)
ttk.Label(main_frame, text="Gender:").grid(row=4, column=0, sticky=tk.W, pady=5)
ttk.Label(main_frame, text="User Type:").grid(row=5, column=0, sticky=tk.W, pady=5)

# Variables
name_var = tk.StringVar()
email_var = tk.StringVar()
age_var = tk.StringVar()
gender_var = tk.StringVar()
user_type = tk.StringVar()

# Entry fields
ttk.Entry(main_frame, textvariable=name_var, width=22).grid(row=1, column=1)
ttk.Entry(main_frame, textvariable=email_var, width=22).grid(row=2, column=1)
ttk.Entry(main_frame, textvariable=age_var, width=22).grid(row=3, column=1)

# Combobox
gender_combo = ttk.Combobox(
    main_frame,
    textvariable=gender_var,
    values=("Male", "Female", "Other"),
    state="readonly",
    width=20
)
gender_combo.current(0)
gender_combo.grid(row=4, column=1)

# Radio buttons
radio_frame = ttk.Frame(main_frame)
radio_frame.grid(row=5, column=1, sticky=tk.W)

ttk.Radiobutton(radio_frame, text="Student", value="Student", variable=user_type).grid(row=0, column=0)
ttk.Radiobutton(radio_frame, text="Teacher", value="Teacher", variable=user_type).grid(row=0, column=1)

# Submit action
def submit_action():
    print(f"""
Name   : {name_var.get()}
Email  : {email_var.get()}
Age    : {age_var.get()}
Gender : {gender_var.get()}
Type   : {user_type.get()}
""")

# Submit button
submit_btn = ttk.Button(main_frame, text="Submit", command=submit_action)
submit_btn.grid(row=6, column=0, columnspan=2, pady=15)

win.mainloop()
