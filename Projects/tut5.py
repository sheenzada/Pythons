from tkinter import *
import time

def show_time():
    t = time.localtime()
    h = t.tm_hour
    m = t.tm_min
    s = t.tm_sec
    am_pm = 'AM' if h<12 else 'PM'
    time_label.config(text=f"{h}:{m}:{s} {am_pm}")
    root.after(1000 , show_time)

root = Tk()
root.geometry("700x400")
root.config(bg="black")

time_label = Label(root, text="",
                       font="Arial 60 bold",
                       bg="black", fg="aqua")
time_label.pack(padx=10 , pady=150)

show_time()
root.mainloop()