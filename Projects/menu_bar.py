import tkinter as tk
from tkinter import  ttk
win = tk.Tk()
win.title('Menubar Tutorial')

def func():
    print('func called')

# MENU
# menu_bar = tk.Menu(win)
# menu_bar.add_command(label='Save' , command=func)
# menu_bar.add_command(label='Save As' , command=func)
# menu_bar.add_command(label='Copy' , command=func)
# menu_bar.add_command(label='Paste' , command=func)

main_menu = tk.Menu(win)
file_menu = tk.Menu(main_menu , tearoff=0)
file_menu.add_command(label='New File' , command=func)
file_menu.add_command(label='New Window' , command=func)
file_menu.add_command(label='Save File' , command=func)

# EDIT MENU
edit_menu = tk.Menu(main_menu , tearoff=0)
edit_menu.add_command(label='Undo', command=func)
edit_menu.add_command(label='Redo', command=func)

main_menu.add_cascade(label='File' , command=file_menu)
main_menu.add_cascade(label='Edit' , command=edit_menu)

win.config(menu=main_menu)

win.mainloop()