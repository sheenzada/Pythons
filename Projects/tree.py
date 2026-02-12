import turtle
t = turtle.Turtle()
t.left(90)
def tree(uzun):
    if uzun < 10: return
    t.forward(uzun)
    t.left(25); tree(uzun*0.7)
    t.right(50); tree(uzun*0.7)
    t.left(25) ; t.backward(uzun)
tree("100")
turtle.done()