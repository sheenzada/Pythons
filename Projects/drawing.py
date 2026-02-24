import turtle
import random

# Initial Setup
screen = turtle.Screen()
screen.bgcolor("black")  # Dark sky
t = turtle.Turtle()
t.speed(0) # 0 is the fastest animation speed

def draw_star(size, x, y, color):
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.color(color)
    t.begin_fill()
    for _ in range(5):
        t.forward(size)
        t.right(144)
    t.end_fill()

def draw_moon(x, y):
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.color("white")
    t.begin_fill()
    t.circle(50)
    t.end_fill()
    
    # "Cut out" the moon by drawing a black circle over it
    t.penup()
    t.goto(x + 20, y)
    t.color("black")
    t.begin_fill()
    t.circle(50)
    t.end_fill()

# --- Execution ---

# 1. Draw a Crescent Moon
draw_moon(150, 100)

# 2. Draw 20 Random Stars
colors = ["yellow", "gold", "white", "lightyellow"]
for _ in range(20):
    rand_x = random.randint(-300, 300)
    rand_y = random.randint(-300, 300)
    rand_size = random.randint(10, 30)
    rand_color = random.choice(colors)
    draw_star(rand_size, rand_x, rand_y, rand_color)

t.hideturtle()
turtle.done()