import tkinter as tk
from tkinter import ttk, filedialog, messagebox, colorchooser, font
import os

# ------------------ MAIN WINDOW ------------------
main_application = tk.Tk()
main_application.geometry("1200x800")
main_application.title("VPad Text Editor")

# This is a transparent 1x1 pixel or placeholder icon logic
# In a real project, you'd use: main_application.iconbitmap('icon.ico')
current_file = None

# ------------------ ICONS (Base64 or Unicode) ------------------
# Using Unicode symbols as icons for portability, but you can replace with PhotoImage
icons = {
    "new": "📄", "open": "📂", "save": "💾", "cut": "✂️", 
    "copy": "📋", "paste": "📥", "find": "🔍", "exit": "❌"
}

# ------------------ MENU BAR ------------------
main_menu = tk.Menu(main_application)

file_menu = tk.Menu(main_menu, tearoff=False)
edit_menu = tk.Menu(main_menu, tearoff=False)
view_menu = tk.Menu(main_menu, tearoff=False)
theme_menu = tk.Menu(main_menu, tearoff=False)

main_menu.add_cascade(label="File", menu=file_menu)
main_menu.add_cascade(label="Edit", menu=edit_menu)
main_menu.add_cascade(label="View", menu=view_menu)
main_menu.add_cascade(label="Color Theme", menu=theme_menu)

# ------------------ TOOL BAR ------------------
tool_bar = ttk.Frame(main_application)
tool_bar.pack(side=tk.TOP, fill=tk.X)

font_tuple = font.families()
font_family = tk.StringVar(value="Arial")
font_size = tk.IntVar(value=12)

font_box = ttk.Combobox(tool_bar, width=30, textvariable=font_family, state="readonly", values=font_tuple)
font_box.grid(row=0, column=0, padx=5, pady=2)

size_box = ttk.Combobox(tool_bar, width=10, textvariable=font_size, state="readonly", values=tuple(range(8, 81)))
size_box.grid(row=0, column=1, padx=5)

# Styling buttons with simple text/unicode for better UI
bold_btn = ttk.Button(tool_bar, text="B")
italic_btn = ttk.Button(tool_bar, text="I")
underline_btn = ttk.Button(tool_bar, text="U")
color_btn = ttk.Button(tool_bar, text="🎨 Color")

bold_btn.grid(row=0, column=2, padx=3)
italic_btn.grid(row=0, column=3, padx=3)
underline_btn.grid(row=0, column=4, padx=3)
color_btn.grid(row=0, column=5, padx=3)

align_left_btn = ttk.Button(tool_bar, text="Left")
align_center_btn = ttk.Button(tool_bar, text="Center")
align_right_btn = ttk.Button(tool_bar, text="Right")

align_left_btn.grid(row=0, column=6, padx=3)
align_center_btn.grid(row=0, column=7, padx=3)
align_right_btn.grid(row=0, column=8, padx=3)

# ------------------ TEXT AREA ------------------
text_frame = ttk.Frame(main_application)
text_frame.pack(fill=tk.BOTH, expand=True)

scroll = ttk.Scrollbar(text_frame)
scroll.pack(side=tk.RIGHT, fill=tk.Y)

text_editor = tk.Text(text_frame, wrap="word", undo=True, yscrollcommand=scroll.set, font=("Arial", 12))
text_editor.pack(fill=tk.BOTH, expand=True)
scroll.config(command=text_editor.yview)

# ------------------ STATUS BAR ------------------
status_bar = ttk.Label(main_application, text="Line: 1 | Column: 1 | Words: 0")
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

# ------------------ FUNCTIONS ------------------

def update_status_bar(event=None):
    if text_editor.edit_modified():
        line, col = text_editor.index(tk.INSERT).split('.')
        content = text_editor.get(1.0, 'end-1c')
        words = len(content.split())
        status_bar.config(text=f"Line: {line} | Column: {int(col)+1} | Words: {words}")
    text_editor.edit_modified(False)

text_editor.bind("<<Modified>>", update_status_bar)
text_editor.bind("<KeyRelease>", update_status_bar)

def new_file(event=None):
    global current_file
    text_editor.delete(1.0, tk.END)
    current_file = None
    main_application.title("VPad - New File")

def open_file(event=None):
    global current_file
    file = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file:
        with open(file, "r") as f:
            text_editor.delete(1.0, tk.END)
            text_editor.insert(tk.END, f.read())
        current_file = file
        main_application.title(os.path.basename(file))

def save_file(event=None):
    global current_file
    if current_file:
        content = text_editor.get(1.0, tk.END)
        with open(current_file, "w") as f:
            f.write(content)
    else:
        save_as_file()

def save_as_file(event=None):
    global current_file
    file = filedialog.asksaveasfilename(defaultextension=".txt")
    if file:
        current_file = file
        with open(file, "w") as f:
            f.write(text_editor.get(1.0, tk.END))
        main_application.title(os.path.basename(file))

def apply_alignment(align_type):
    # This creates a tag for the alignment and applies it to the whole line
    text_editor.tag_configure(align_type, justify=align_type)
    text_editor.tag_add(align_type, "insert linestart", "insert lineend")

def toggle_bold():
    curr_font = font.Font(font=text_editor['font'])
    if curr_font.actual()['weight'] == 'normal':
        text_editor.configure(font=(font_family.get(), font_size.get(), 'bold'))
    else:
        text_editor.configure(font=(font_family.get(), font_size.get(), 'normal'))

# ------------------ THEMES ------------------
themes = {
    "Light": ("#000000", "#ffffff"),
    "Dark": ("#ffffff", "#2d2d2d"),
    "Monokai": ("#F8F8F2", "#272822"),
    "Solarized": ("#657b83", "#fdf6e3")
}

def change_theme():
    fg, bg = themes[theme_choice.get()]
    text_editor.config(fg=fg, bg=bg, insertbackground=fg) # insertbackground is the cursor color

theme_choice = tk.StringVar()
for theme in themes:
    theme_menu.add_radiobutton(label=theme, variable=theme_choice, command=change_theme)

# ------------------ MENU COMMANDS ------------------
file_menu.add_command(label="New", accelerator="Ctrl+N", command=new_file)
file_menu.add_command(label="Open", accelerator="Ctrl+O", command=open_file)
file_menu.add_command(label="Save", accelerator="Ctrl+S", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=main_application.quit)

edit_menu.add_command(label="Copy", accelerator="Ctrl+C", command=lambda: text_editor.event_generate("<<Copy>>"))
edit_menu.add_command(label="Paste", accelerator="Ctrl+V", command=lambda: text_editor.event_generate("<<Paste>>"))
edit_menu.add_command(label="Cut", accelerator="Ctrl+X", command=lambda: text_editor.event_generate("<<Cut>>"))
edit_menu.add_command(label="Clear All", command=lambda: text_editor.delete(1.0, tk.END))

# ------------------ BINDINGS & BUTTONS ------------------
main_application.bind("<Control-n>", new_file)
main_application.bind("<Control-o>", open_file)
main_application.bind("<Control-s>", save_file)

font_box.bind("<<ComboboxSelected>>", lambda e: text_editor.configure(font=(font_family.get(), font_size.get())))
size_box.bind("<<ComboboxSelected>>", lambda e: text_editor.configure(font=(font_family.get(), font_size.get())))

bold_btn.configure(command=toggle_bold)
align_left_btn.configure(command=lambda: apply_alignment('left'))
align_center_btn.configure(command=lambda: apply_alignment('center'))
align_right_btn.configure(command=lambda: apply_alignment('right'))
color_btn.configure(command=lambda: text_editor.config(fg=colorchooser.askcolor()[1]))

main_application.config(menu=main_menu)
main_application.mainloop()