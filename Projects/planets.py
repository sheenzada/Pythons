import tkinter as tk
import math
import random

WIDTH = 900
HEIGHT = 700

root = tk.Tk()
root.title("Dancing Planets")

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
canvas.pack()

cx = WIDTH // 2
cy = HEIGHT // 2

# Sun
canvas.create_oval(
    cx - 40, cy - 40,
    cx + 40, cy + 40,
    fill="gold",
    outline="yellow",
    width=3
)

planets = []

for i in range(8):
    planet = {
        "angle": random.uniform(0, 360),
        "orbit": 80 + i * 50,
        "speed": random.uniform(0.01, 0.05),
        "size": random.randint(12, 25),
        "obj": canvas.create_oval(0, 0, 0, 0)
    }
    planets.append(planet)

frame = 0

def rainbow(t):
    r = int(128 + 127 * math.sin(t))
    g = int(128 + 127 * math.sin(t + 2))
    b = int(128 + 127 * math.sin(t + 4))
    return f"#{r:02x}{g:02x}{b:02x}"

def animate():
    global frame
    frame += 1

    for i, p in enumerate(planets):

        p["angle"] += p["speed"]

        # Crazy dancing motion
        x = cx + (
            p["orbit"] * math.cos(p["angle"])
            + 40 * math.sin(frame * 0.05 + i)
        )

        y = cy + (
            p["orbit"] * math.sin(p["angle"])
            + 40 * math.cos(frame * 0.04 + i * 2)
        )

        # Pulsing size
        size = p["size"] + 5 * math.sin(frame * 0.1 + i)

        color = rainbow(frame * 0.05 + i)

        canvas.coords(
            p["obj"],
            x - size,
            y - size,
            x + size,
            y + size
        )

        canvas.itemconfig(
            p["obj"],
            fill=color,
            outline="white"
        )

    root.after(16, animate)

animate()
root.mainloop()