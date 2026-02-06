import tkinter as tk
from tkinter import ttk
win = tk.Tk()
win.title ('GUI')

# Creat Labels
name_label = ttk.Label(win , text='Enter Your Name ?')
name_label.grid(row=0 , column=0 , sticky=tk.W)

eamil_label = ttk.Label(win , text= ' Enter Your Email ?')
eamil_label.grid(column=0 , row=1 , sticky=tk.W)

age_label = ttk.Label(win , text= ' Enter Your Age ?')
age_label.grid(column=0 , row=2 , sticky=tk.W)

gender_label = ttk.Label(win , text= 'Select Your Gender :')
gender_label.grid(column=0 , row=3 , sticky=tk.W)
# Create entry box

name_var = tk.StringVar()
name_entrybox = ttk.Entry(win , textvariable=name_var , width=16)
name_entrybox.grid(row=0  , column=1)

email_var = tk.StringVar()
email_entrybox = ttk.Entry(win , textvariable=email_var , width=16)
email_entrybox.grid(row=1  , column=1)

age_var = tk.StringVar()
age_entrybox = ttk.Entry(win , textvariable=age_var , width=16)
age_entrybox.grid(row=2  , column=1)

gender_var = tk.StringVar()
gender_combobox = ttk.Combobox(win , width=16 , textvariable=gender_var , state='readonly' )
gender_combobox['values']= ('Male' , 'Female' , 'Other')
gender_combobox.current(0)
gender_combobox.grid(row=3 , column=1)
 

user_type = tk.StringVar()
radiobtn1 =  ttk.Radiobutton(win, text='Student' , value='Student' , variable=user_type)
radiobtn1.grid(row=4 , column=0)

radiobtn2 = ttk.Radiobutton(win, text='Teacher' , value = 'Teacher' , variable=user_type)
radiobtn2.grid(row= 5 , column=0)

# Check Button
checkbtn_var = tk.IntVar()

checkbtn = ttk.Checkbutton(win , text='check if you want to subscribe to our newsletter' , variable=checkbtn_var)
checkbtn.grid(row=6 , columnspan=3)



def action ():
    user_name = name_var.get()
    user_age = age_var.get()
    user_email = email_var.get()
    print(f' {user_name} is {user_age} years old, {user_email} ')
    user_gender = gender_var.get()
    user_type = user_type.get()
    if checkbtn_var.get() == 0:
        subscribed = 'NO'
    else:
        subscribed = 'Yes'
    print(user_gender , user_type , subscribed)
submit_btn = ttk.Button(win , text='Sumbit' , command=action)
submit_btn.grid(row=8 , column=0)
win.mainloop()