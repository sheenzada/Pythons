import turtle

# Set up the screen
screen = turtle.Screen()
screen.title("Python Smiley Face")
t = turtle.Turtle()
t.speed(3)

def draw_circle(color, radius, x, y):
    t.penup()
    t.fillcolor(color)
    t.goto(x, y)
    t.pendown()
    t.begin_fill()
    t.circle(radius)
    t.end_fill()

# 1. Draw the face (Yellow Circle)
draw_circle("yellow", 100, 0, -100)

# 2. Draw the left eye
draw_circle("black", 15, -35, 30)

# 3. Draw the right eye
draw_circle("black", 15, 35, 30)

# 4. Draw the smile (A semi-circle)
t.penup()
t.goto(-60, -10)
t.setheading(-60) # Tilt the turtle to start the curve
t.width(5)
t.pendown()
t.circle(70, 120) # Draw 120 degrees of a circle with radius 70

# Hide the turtle and finish
t.hideturtle()
turtle.done()