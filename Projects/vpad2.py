import tkinter as tk
from tkinter import ttk, filedialog, messagebox, colorchooser, font
import os

# ------------------ MAIN WINDOW ------------------
main_application = tk.Tk()
main_application.geometry("1200x800")
main_application.title("VPad Text Editor")

current_file = None

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

font_family = tk.StringVar()
font_size = tk.IntVar()

font_box = ttk.Combobox(
    tool_bar,
    width=30,
    textvariable=font_family,
    state="readonly",
    values=font.families()
)
font_box.set("Arial")
font_box.grid(row=0, column=0, padx=5)

size_box = ttk.Combobox(
    tool_bar,
    width=10,
    textvariable=font_size,
    state="readonly",
    values=tuple(range(8, 81))
)
size_box.set(12)
size_box.grid(row=0, column=1, padx=5)

bold_btn = ttk.Button(tool_bar, text="B")
italic_btn = ttk.Button(tool_bar, text="I")
underline_btn = ttk.Button(tool_bar, text="U")
color_btn = ttk.Button(tool_bar, text="Color")

bold_btn.grid(row=0, column=2, padx=5)
italic_btn.grid(row=0, column=3, padx=5)
underline_btn.grid(row=0, column=4, padx=5)
color_btn.grid(row=0, column=5, padx=5)

# ------------------ TEXT AREA ------------------
text_editor = tk.Text(main_application, wrap="word", undo=True)
text_editor.pack(fill=tk.BOTH, expand=True)

scroll = ttk.Scrollbar(text_editor, command=text_editor.yview)
scroll.pack(side=tk.RIGHT, fill=tk.Y)
text_editor.config(yscrollcommand=scroll.set)

current_font = font.Font(family="Arial", size=12)
text_editor.configure(font=current_font)

# ------------------ STATUS BAR ------------------
status_bar = ttk.Label(main_application, text="Ready")
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

# ------------------ FUNCTIONS ------------------
def new_file():
    global current_file
    text_editor.delete(1.0, tk.END)
    current_file = None
    main_application.title("VPad Text Editor")

def open_file():
    global current_file
    file = filedialog.askopenfilename()
    if file:
        with open(file, "r", encoding="utf-8") as f:
            text_editor.delete(1.0, tk.END)
            text_editor.insert(tk.END, f.read())
        current_file = file
        main_application.title(os.path.basename(file))

def save_file():
    global current_file
    if current_file:
        with open(current_file, "w", encoding="utf-8") as f:
            f.write(text_editor.get(1.0, tk.END))
    else:
        save_as_file()

def save_as_file():
    global current_file
    file = filedialog.asksaveasfilename(defaultextension=".txt")
    if file:
        current_file = file
        save_file()
        main_application.title(os.path.basename(file))

def exit_app():
    main_application.destroy()

def change_font_family(event=None):
    current_font.config(family=font_family.get())

def change_font_size(event=None):
    current_font.config(size=font_size.get())

def toggle_bold():
    current_font.config(weight="bold" if current_font.actual()["weight"] == "normal" else "normal")

def toggle_italic():
    current_font.config(slant="italic" if current_font.actual()["slant"] == "roman" else "roman")

def toggle_underline():
    current_font.config(underline=0 if current_font.actual()["underline"] else 1)

def font_color():
    color = colorchooser.askcolor()[1]
    if color:
        text_editor.config(fg=color)

def clear_all():
    text_editor.delete(1.0, tk.END)

def find_text():
    find_window = tk.Toplevel()
    find_window.title("Find")

    tk.Label(find_window, text="Find:").pack(side=tk.LEFT, padx=5)
    find_entry = ttk.Entry(find_window)
    find_entry.pack(side=tk.LEFT, padx=5)

    def search():
        text_editor.tag_remove("match", "1.0", tk.END)
        word = find_entry.get()
        if word:
            start = "1.0"
            while True:
                pos = text_editor.search(word, start, tk.END)
                if not pos:
                    break
                end = f"{pos}+{len(word)}c"
                text_editor.tag_add("match", pos, end)
                start = end
            text_editor.tag_config("match", background="yellow")

    ttk.Button(find_window, text="Find", command=search).pack(side=tk.LEFT)

# ------------------ COLOR THEMES ------------------
themes = {
    "Light": ("#000000", "#ffffff"),
    "Dark": ("#ffffff", "#2d2d2d"),
    "Red": ("#2d2d2d", "#ffe8e8"),
    "Night Blue": ("#ededed", "#6b9dc2")
}

theme_choice = tk.StringVar()

def change_theme():
    fg, bg = themes[theme_choice.get()]
    text_editor.config(fg=fg, bg=bg)

for theme in themes:
    theme_menu.add_radiobutton(
        label=theme,
        variable=theme_choice,
        value=theme,
        command=change_theme
    )

# ------------------ MENU COMMANDS ------------------
file_menu.add_command(label="New", command=new_file, accelerator="Ctrl+N")
file_menu.add_command(label="Open", command=open_file, accelerator="Ctrl+O")
file_menu.add_command(label="Save", command=save_file, accelerator="Ctrl+S")
file_menu.add_command(label="Save As", command=save_as_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_app)

edit_menu.add_command(label="Copy", command=lambda: text_editor.event_generate("<<Copy>>"))
edit_menu.add_command(label="Paste", command=lambda: text_editor.event_generate("<<Paste>>"))
edit_menu.add_command(label="Cut", command=lambda: text_editor.event_generate("<<Cut>>"))
edit_menu.add_command(label="Clear All", command=clear_all)
edit_menu.add_command(label="Find", command=find_text)

# ------------------ BINDINGS ------------------
font_box.bind("<<ComboboxSelected>>", change_font_family)
size_box.bind("<<ComboboxSelected>>", change_font_size)

bold_btn.config(command=toggle_bold)
italic_btn.config(command=toggle_italic)
underline_btn.config(command=toggle_underline)
color_btn.config(command=font_color)

main_application.config(menu=main_menu)
main_application.mainloop()
