import tkinter as tk
from tkinter import ttk
win = tk.Tk()
win.title('LOOP')

labels = ['What is Yout Name :' , 'What is Your Age : ' , 'What is Your Gender' , 'Country' , 'State' , 'City' , 'address']
# name_lable = ttk.Label(win, text = 'What is Your Name ?')
# name_lable.grid(row = 0 , column=0 , sticky=tk.W) 

for i in range (len(labels)):
    cur_label = 'label' + str(i) 
    cur_lable = ttk.Label(win, text = labels[i])
    cur_lable.grid(row = i , column=0 , sticky=tk.W) 


nam_var = tk.StringVar()
user_info = {
    'name': tk.StringVar(),
    'age': tk.StringVar(),
    'gender': tk.StringVar(),
    'country': tk.StringVar(),
    'state': tk.StringVar(),
    'city': tk.StringVar(),
    'address' : tk.StringVar(),
}
counter = 0
for i in user_info :
    cur_entrybox = 'entry' + i
    cur_entrybox = ttk.Entry(win , width=16 , textvariable=user_info[i])
    cur_entrybox.grid(column=1 , row=counter)
    counter += 1

def submit ():
    print(user_info['name'].get())
    print(user_info.get('age').get())
    print(user_info.get('gender').get())
    print(user_info.get('country').get())
    print(user_info.get('state').get())
    print(user_info.get('city').get())
    print(user_info.get('address').get())
submit_btn = ttk.Button(win , text='Submit' , command=submit)
submit_btn.grid (row=8 , columnspan=2 )
win.mainloop()
