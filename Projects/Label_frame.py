import tkinter as tk
from tkinter import ttk
win =tk.Tk()
win.title("LOOP")

labels = ['What is your Name :' , 'What is your Age :' , 'What is your Sex : ' , 'Country :' , 'State' , 'City' , 'Address']

for i in range (len(labels)):
    cur_label = 'label' + str(i)
    cur_label = ttk.Label(win ,text=labels[i])
    cur_label.grid(row= i , column=0 , sticky=tk.W , padx=40 , pady=50)

# entry box

name_var = tk.StringVar()
user_info = {
    'name': tk.StringVar(),
    'age':tk.StringVar(),
    'sex':tk.StringVar(),
    'country':tk.StringVar(),
    'state':tk.StringVar(),
    'city':tk.StringVar(),
    'address':tk.StringVar()
}
counter = 0
for i in user_info:
     cur_entrybox = 'entry' + i
     cur_entrybox = ttk.Entry(win , width=16 , textvariable=user_info[i])
     cur_entrybox.grid(row=counter , column=1 , padx=2 ,pady=2)
     counter += 1
def submit():
     print(user_info['name'].get())
     print(user_info.get()['age'].get())
     print(user_info.get()['sex'].get())
     print(user_info.get()['country'].get())
     print(user_info.get()['state'].get())
     print(user_info.get()['city'].get())
submit_btn = ttk.Button(win , text='Submit' , command=submit)
submit_btn.grid(row=7 , columnspan=2)

win.mainloop()