import tkinter as tk
from tkinter import colorchooser, filedialog, simpledialog
from PIL import Image, ImageDraw, ImageTk
import os


class PaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Paint App")
        self.root.geometry("1200x750")

        # Variables
        self.current_color = "black"
        self.brush_size = 5
        self.tool = "brush"
        self.start_x = None
        self.start_y = None

        self.undo_stack = []
        self.redo_stack = []

        self.image = Image.new("RGB", (1200, 650), "white")
        self.draw = ImageDraw.Draw(self.image)

        self.setup_ui()
        self.update_canvas()

    # ---------------- UI ---------------- #
    def setup_ui(self):
        toolbar = tk.Frame(self.root, bg="#dddddd", height=50)
        toolbar.pack(fill=tk.X)

        tk.Button(toolbar, text="Brush", command=lambda: self.set_tool("brush")).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar, text="Eraser", command=lambda: self.set_tool("eraser")).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar, text="Line", command=lambda: self.set_tool("line")).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar, text="Rectangle", command=lambda: self.set_tool("rectangle")).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar, text="Circle", command=lambda: self.set_tool("circle")).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar, text="Text", command=lambda: self.set_tool("text")).pack(side=tk.LEFT, padx=2)

        tk.Button(toolbar, text="Color", command=self.choose_color).pack(side=tk.LEFT, padx=10)

        self.size_slider = tk.Scale(toolbar, from_=1, to=50, orient=tk.HORIZONTAL, label="Size")
        self.size_slider.set(self.brush_size)
        self.size_slider.pack(side=tk.LEFT)

        tk.Button(toolbar, text="Undo", command=self.undo).pack(side=tk.LEFT, padx=5)
        tk.Button(toolbar, text="Redo", command=self.redo).pack(side=tk.LEFT, padx=5)
        tk.Button(toolbar, text="Clear", command=self.clear_canvas).pack(side=tk.LEFT, padx=5)
        tk.Button(toolbar, text="Open", command=self.open_image).pack(side=tk.LEFT, padx=5)
        tk.Button(toolbar, text="Save", command=self.save_image).pack(side=tk.LEFT, padx=5)

        self.canvas = tk.Canvas(self.root, bg="white", cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw_motion)
        self.canvas.bind("<ButtonRelease-1>", self.end_draw)

    # ---------------- Tools ---------------- #
    def set_tool(self, tool):
        self.tool = tool

    def choose_color(self):
        color = colorchooser.askcolor(color=self.current_color)
        if color[1]:
            self.current_color = color[1]

    # ---------------- Drawing Logic ---------------- #
    def start_draw(self, event):
        self.save_undo()
        self.start_x = event.x
        self.start_y = event.y

        if self.tool == "text":
            text = simpledialog.askstring("Text", "Enter text:")
            if text:
                self.draw.text((event.x, event.y), text, fill=self.current_color)
                self.update_canvas()

    def draw_motion(self, event):
        size = self.size_slider.get()
        color = "white" if self.tool == "eraser" else self.current_color

        if self.tool in ["brush", "eraser"]:
            self.draw.line(
                [self.start_x, self.start_y, event.x, event.y],
                fill=color,
                width=size
            )
            self.start_x = event.x
            self.start_y = event.y
            self.update_canvas()

    def end_draw(self, event):
        size = self.size_slider.get()

        if self.tool == "line":
            self.draw.line([self.start_x, self.start_y, event.x, event.y],
                           fill=self.current_color, width=size)

        elif self.tool == "rectangle":
            self.draw.rectangle([self.start_x, self.start_y, event.x, event.y],
                                outline=self.current_color, width=size)

        elif self.tool == "circle":
            self.draw.ellipse([self.start_x, self.start_y, event.x, event.y],
                              outline=self.current_color, width=size)

        self.update_canvas()

    # ---------------- Canvas Update ---------------- #
    def update_canvas(self):
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.tk_image, anchor=tk.NW)

    # ---------------- Undo / Redo ---------------- #
    def save_undo(self):
        self.undo_stack.append(self.image.copy())
        self.redo_stack.clear()

    def undo(self):
        if self.undo_stack:
            self.redo_stack.append(self.image.copy())
            self.image = self.undo_stack.pop()
            self.draw = ImageDraw.Draw(self.image)
            self.update_canvas()

    def redo(self):
        if self.redo_stack:
            self.undo_stack.append(self.image.copy())
            self.image = self.redo_stack.pop()
            self.draw = ImageDraw.Draw(self.image)
            self.update_canvas()

    # ---------------- File Operations ---------------- #
    def clear_canvas(self):
        self.save_undo()
        self.image = Image.new("RGB", (1200, 650), "white")
        self.draw = ImageDraw.Draw(self.image)
        self.update_canvas()

    def save_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG files", "*.png")])
        if file_path:
            self.image.save(file_path)

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
        if file_path:
            img = Image.open(file_path)
            self.image = img.resize((1200, 650))
            self.draw = ImageDraw.Draw(self.image)
            self.update_canvas()


# ---------------- Run App ---------------- #
if __name__ == "__main__":
    root = tk.Tk()
    app = PaintApp(root)
    root.mainloop()
