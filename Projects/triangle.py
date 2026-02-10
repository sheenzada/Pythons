from turtle import *

bgcolor("black")
tracer(2)
color("pink")

points = [(-200 , -150) , (0 , 200) , (200 , -150)]

hideturtle()

def draw_triangle(points):
    up()
    goto(points[0])
    down()
    goto(points[1])
    goto(points[2])
    goto(points[0])
def get_mid(p1,p2):
    return((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) /2)
def sierpinski(points , depth):
    if depth == 0:
        draw_triangle(points)
    else:
        mid1 = get_mid(points[0] , points[1])
        mid2 = get_mid(points[1] , points[2])
        mid3 = get_mid(points[2] , points[0])

        sierpinski([points[0] , mid1 , mid3], depth -1)
        sierpinski([mid1 , points[1] , mid2], depth -1)
        sierpinski([mid3, mid2 , points[2]], depth -1)
sierpinski(points, 6)

mainloop()