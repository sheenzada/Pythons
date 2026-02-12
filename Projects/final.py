import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as m_box
win = tk.Tk()

# label frames

label_frame = ttk.LabelFrame(win , text='Contact Details')
label_frame.grid(row= 0 , column=0 , padx=40 , pady=10)

# labels

name_labels = ttk.Label(label_frame , text='Enter Your Name Please :' , font='Helvetica')
age_labels = ttk.Label(label_frame , text='Enter Your Age Please :' , font='Helvetica' )

# entry box variables

name_var = tk.StringVar()
age_var = tk.StringVar()

# entry boxes

name_entry = tk.Entry(label_frame , width=36 , textvariable=name_var)
age_entry = tk.Entry(label_frame , width=36 , textvariable=age_var)

# grid

name_labels.grid(row= 0 , column= 0 , padx=5 , pady=5 , sticky=tk.W)
age_labels.grid(row= 0 , column= 1 , padx=5 , pady=5 , sticky=tk.W)
name_entry.grid(row= 1 , column= 0 , padx=5 , pady=5 , sticky=tk.W)
age_entry.grid(row= 1 , column= 1 , padx=5 , pady=5 , sticky=tk.W)

def submit():
    # m_box.showwarning('title' , 'content of this message box !! ❌')
    name = name_var.get()
    age = age_var.get()
    if name == '' or age == '':
     m_box.showwarning('Error' , 'Please fill both name and age !! ❌')
    else:
       try:
          age = int(age)
       except ValueError:
          m_box.showerror('title' , 'Only digits are allowed in age field')
       else:
          if age > 18:
            m_box.showwarning('Warning' , 'you are not 18 , visit this contenet on own your own risk')
          print(f'{name} : {age}')
  




submit_btn = ttk.Button(win ,text='Submit' , command=submit)
submit_btn.grid(row=1 , columnspan=2 , padx=40) 
win.mainloop()



