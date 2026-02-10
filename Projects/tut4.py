from tkinter import *
from PIL import Image , ImageTk

root = Tk()

root.geometry("500x600")

image = Image.open('img/inam.jpg')

photo = ImageTk.PhotoImage(image)
Label(image=photo).pack()
root.mainloop()