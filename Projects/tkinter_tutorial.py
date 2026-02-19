import tkinter as tk
from tkinter import ttk
win = tk.Tk()
win.title('GUI')

# create labels

name_label = tk.Label(win , text='Enter Your Name :')
name_label.grid(row=0 , column=0 , sticky=tk.W)

email_label = tk.Label(win , text='Enter Your email :')
email_label.grid(row=1 , column=0 , sticky=tk.W)

age_label = tk.Label(win , text='Enter Your age :')
age_label.grid(row=2 , column=0 , sticky=tk.W)

gender_label = tk.Label(win , text='Select Your Sex:')
gender_label.grid(row=3 , column=0 , sticky=tk.W)

# create entry box
name_var = tk.StringVar()
name_entrybox = ttk.Entry(win , width=16 , textvariable=name_var)
name_entrybox.grid(row=0 , column=1)

email_var = tk.StringVar()
email_entrybox = ttk.Entry(win , width=16 , textvariable=email_var)
email_entrybox.grid(row=1 , column=1)

age_var = tk.StringVar()
age_entrybox = ttk.Entry(win , width=16 , textvariable=age_var)
age_entrybox.grid(row=2 , column=1)

# create combobox

gender_combobox = ttk.Combobox(win , width=16)
gender_combobox['values'] = ('Male' ,'Female' , 'Other')
gender_combobox.grid(row=3 , column=1)

# create button

def action():
    
    username = name_var.get()
    userage = age_var.get()
    useremail = email_var.get()
    print(f'{username} is {userage} years old , and his email is {useremail}')
submit_button = ttk.Button(win , text='Submit' , command=action)
submit_button.grid(row=3 , column=0)

win.mainloop()