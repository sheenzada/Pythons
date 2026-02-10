from tkinter import *

root = Tk()
root.geometry("500x500")

def hello ():
    print("Button Clicked")
text = Label(text='Click The Button' , font='Arial 13 bold')

text.pack(padx=20 , pady=20)

btn = Button(text='Click Me!' , command=hello)
btn.pack()
root.mainloop()