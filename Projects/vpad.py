import tkinter as tk
from tkinter import ttk
from tkinter import font, colorchooser , filedialog , messagebox
import os

main_application = tk.Tk()
main_application.geometry("1200x800")
main_application.title('Vpad text editor')

################################ MAIN MENU #############################
#------------------------------- END MAIN MENU ------------------------#

main_menu = tk.Menu()
# file icons
new_icon = tk.PhotoImage(file='img/logo.png')
open_icon = tk.PhotoImage(file='img/like-heart-round-line-icon.png')
save_icon = tk.PhotoImage(file='')
save_as_icon = tk.PhotoImage(file='')
exit_icon = tk.PhotoImage(file='img/img/menuicon.png')


file = tk.Menu(main_menu , tearoff=False )


# EDIT ICONS
copy_icon = tk.PhotoImage(file='img/logo.png')
paste_icon = tk.PhotoImage(file='img/img/menuicon.png')
cut_icon = tk.PhotoImage(file='')
clear_all_icon = tk.PhotoImage(file='')
find_icon = tk.PhotoImage(file='')

edit = tk.Menu(main_menu , tearoff=False)

# VIEW ICONS
tool_bar_icon = tk.PhotoImage(file='img/logo.png')
status_bar_icon = tk.PhotoImage(file='img/img/menuicon.png')
view = tk.Menu(main_menu , tearoff=False)

# COLOR THEME
light_default_icon = tk.PhotoImage(file='img/img/logo.png')
light_plus_icon = tk.PhotoImage(file='img/img/menuicon.png')
dark_icon = tk.PhotoImage(file='img/img/menuicon.png')
red_icon = tk.PhotoImage(file='img/img/menuicon.png')
monokia_icon = tk.PhotoImage(file='img/img/menuicon.png')
night_blue_icon = tk.PhotoImage(file='img/img/menuicon.png')
color_theme = tk.Menu(main_menu , tearoff=False)

theme_choice = tk.StringVar()
color_icons = (light_default_icon , light_plus_icon , dark_icon , red_icon , monokia_icon , night_blue_icon )

color_dict = {
    ' Light Default ' : ('#000000' , '#ffffff'),
    ' Light Plus' : ('#474747' , '#e0e0e0'),
    'Dark' : ('#c4c4c4' , '#2d2d2d'),
    'Red' : ('#2d2d2d' , '#ffe8e8'),
    'Monokia' : ('#d3b774' , '#474747'),
    'Night Blue' : ('#ededed' , '#6b9dc2'),
}

# cascade

main_menu.add_cascade(label='File' , menu=file)
main_menu.add_cascade(label='Edit' , menu=edit)
main_menu.add_cascade(label='View' , menu=view)
main_menu.add_cascade(label='Color Theme' , menu=color_theme)


################################# Tool Bar #############################
#-------------------------------- End Tool Bar ------------------------#
# print(type(tk.font.families()))

tool_bar = ttk.Label(main_application)
tool_bar.pack(side=tk.TOP, fill=tk.X)


# font box
font_tuples= tk.font.families()
font_family = tk.StringVar()
font_box = ttk.Combobox(tool_bar , width=30 , textvariable=font_family , state='readonly')
font_box['values'] = font_tuples
# font_box.current(0)
font_box.current(font_tuples.index('Arial'))
font_box.grid(row= 0 , column= 0 , padx=5)

# size box
size_var = tk.IntVar()
font_size = ttk.Combobox(tool_bar , width=14 , textvariable= size_var , state='readonly')
font_size['values'] = tuple(range(8 , 81))
font_size.current(4)
font_size.grid(row=0 , column=1 , padx=5)

# Bold Button
bold_icon = tk.PhotoImage(file='img/logo.png')
bold_button = ttk.Button(tool_bar , image=bold_icon)
bold_button.grid(row=0 , column=2 , padx=5)

# Italic Button
italic_icon = tk.PhotoImage(file='img/img/menuicon.png')
italic_btn = ttk.Button(tool_bar , image=italic_icon)
italic_btn.grid(row= 0 , column=4 , padx=5)

# Underline Button
underline_icon = tk.PhotoImage(file='img/logo.png')
underline_btn = ttk.Button(tool_bar , image=underline_icon)
underline_btn.grid(row=0 , column=5 , padx=5)

# Font color button
font_color_icon = tk.PhotoImage(file='img/img/menuicon.png')
font_color_btn = ttk.Button(tool_bar , image=font_color_icon)
font_color_btn.grid(row=0 , column=5 , padx=5)

# align left
align_left_icon = tk.PhotoImage(file='img/img/menuicon.png')
align_left_btn = ttk.Button(tool_bar , image=align_left_icon)
align_left_btn.grid(row=0 , column=6 , padx=5)

# align center
align_center_icon = tk.PhotoImage(file='img/logo.png')
align_center_btn = ttk.Button(tool_bar , image=align_center_icon)
align_center_btn.grid(row=0 , column=7 , padx=5)

# align right
align_right_icon = tk.PhotoImage(file='img/logo.png')
align_right_btn = ttk.Button(tool_bar , image=align_right_icon)
align_right_btn.grid(row=0 , column=8 , padx=5)


################### End tool Bar#####################
#------------------ TEXT EDITOR---------------------#
text_editor = tk.Text(main_application)
text_editor.config(wrap='word' , relief=tk.FLAT)

scroll_bar = tk.Scrollbar(main_application)
text_editor.focus_set()
scroll_bar.pack(side=tk.RIGHT , fill=tk.Y)
text_editor.pack(fill=tk.BOTH , expand=True)
scroll_bar.config(command=text_editor.yview)
text_editor.config(yscrollcommand=scroll_bar.set)

############# font family and font size functionality
current_font_family = 'Arail'
current_font_size = 12

def change_font(main_application):
    global current_font_family
    current_font_family = font_family.get()
    text_editor.configure(font=(current_font_family , current_font_size))

def change_fontsize(main_application):
    global current_font_family
    current_font_size = size_var.get()
    text_editor.configure(font=(current_font_family , current_font_size))
    
font_box.bind("<<comboboxSelected>>" , change_font)
font_size.bind("<<comboboxSelected>>" , change_fontsize)

######## buttons functionality

######## bold button functionality
def change_bold():
    text_property = tk.font.FONT(font = text_editor['font'])
    if text_property.actual()['weight'] == 'normal':
        text_editor.configure(font=(current_font_family , current_font_size , 'bold'))
    if text_property.actual()['weight'] == 'bold':
        text_editor.configure(font=(current_font_family , current_font_size , 'normal'))

bold_button.configure(command=change_bold)

text_editor.configure(font=('Arial' , 12))

#-------------------------&&&&&& End Text Editor----------#

############################## Status Bar ##############################
status_bar = ttk.Label(main_application , text='Status Bar')
status_bar.pack(side=tk.BOTTOM)


##-- file commands
file.add_command(label='New' , image=new_icon , compound = tk.LEFT , accelerator = 'Ctrl+N')
file.add_command(label='Open' , image=new_icon , compound = tk.LEFT , accelerator = 'Ctrl+O')
file.add_command(label='Save' , image=new_icon , compound = tk.LEFT , accelerator = 'Ctrl+S')
file.add_command(label='Save As' , image=new_icon , compound = tk.LEFT , accelerator = 'Ctrl+Alt+S')
file.add_command(label='Exit' , image=new_icon , compound = tk.LEFT , accelerator = 'Ctrl+Q')

## --- Edit commands
edit.add_command(label='Copy' , image=copy_icon , compound=tk.LEFT , accelerator='Ctrl+C')
edit.add_command(label='Paste' , image=paste_icon , compound=tk.LEFT , accelerator='Ctrl+V')
edit.add_command(label='Cut' , image=cut_icon , compound=tk.LEFT , accelerator='Ctrl+X')
edit.add_command(label='Clear All' , image=clear_all_icon , compound=tk.LEFT , accelerator='Ctrl+Alt+X')
edit.add_command(label='Find' , image=find_icon , compound=tk.LEFT , accelerator='Ctrl+F')

## --- View check button
view.add_checkbutton(label='Tool Bar' , image=tool_bar_icon , compound=tk.LEFT)
view.add_checkbutton(label='Status Bar' , image=status_bar_icon , compound=tk.LEFT)

## --- color theme
count = 0
for i in color_dict:
    color_theme.add_radiobutton(label = i, image=color_icons[count] , variable=theme_choice , compound=tk.LEFT)
    count += 1


main_application.config(menu=main_menu)
main_application.mainloop()