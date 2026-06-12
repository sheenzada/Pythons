import tkinter as tk
import math
import time

WIDTH = 500
HEIGHT = 500
CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2
RADIUS = 200

root = tk.Tk()
root.title("Analog Clock")
root.resizable(False, False)

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
canvas.pack()

# Draw clock face
canvas.create_oval(
    CENTER_X - RADIUS,
    CENTER_Y - RADIUS,
    CENTER_X + RADIUS,
    CENTER_Y + RADIUS,
    outline="white",
    width=4
)

# Draw numbers
for i in range(1, 13):
    angle = math.radians(i * 30 - 90)
    x = CENTER_X + math.cos(angle) * (RADIUS - 30)
    y = CENTER_Y + math.sin(angle) * (RADIUS - 30)

    canvas.create_text(
        x, y,
        text=str(i),
        fill="white",
        font=("Arial", 18, "bold")
    )

# Create hands
hour_hand = canvas.create_line(
    CENTER_X, CENTER_Y,
    CENTER_X, CENTER_Y - 80,
    fill="white",
    width=6
)

minute_hand = canvas.create_line(
    CENTER_X, CENTER_Y,
    CENTER_X, CENTER_Y - 120,
    fill="cyan",
    width=4
)

second_hand = canvas.create_line(
    CENTER_X, CENTER_Y,
    CENTER_X, CENTER_Y - 150,
    fill="red",
    width=2
)

def update_clock():
    now = time.localtime()

    sec = now.tm_sec
    minute = now.tm_min + sec / 60
    hour = (now.tm_hour % 12) + minute / 60

    sec_angle = math.radians(sec * 6 - 90)
    min_angle = math.radians(minute * 6 - 90)
    hour_angle = math.radians(hour * 30 - 90)

    # Second hand
    sx = CENTER_X + math.cos(sec_angle) * 150
    sy = CENTER_Y + math.sin(sec_angle) * 150
    canvas.coords(second_hand, CENTER_X, CENTER_Y, sx, sy)

    # Minute hand
    mx = CENTER_X + math.cos(min_angle) * 120
    my = CENTER_Y + math.sin(min_angle) * 120
    canvas.coords(minute_hand, CENTER_X, CENTER_Y, mx, my)

    # Hour hand
    hx = CENTER_X + math.cos(hour_angle) * 90
    hy = CENTER_Y + math.sin(hour_angle) * 90
    canvas.coords(hour_hand, CENTER_X, CENTER_Y, hx, hy)

    root.after(1000, update_clock)

update_clock()

root.mainloop()