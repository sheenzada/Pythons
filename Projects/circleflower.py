from turtle import *
import colorsys as cs

tracer (60)
bgcolor("purple")
hideturtle()
pensize(1.5)

for i in  range(600):
    color(cs.hsv_to_rgb(i / 450 , 1 ,1))
    circle(i* 0.4, 120)
    right(70)
    forward(i*0.3)
    left(150)
    circle(i*0.2)
done()