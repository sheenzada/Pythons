import pygame
import math
pygame.init()

WIDTH , HEIGHT = 1200 , 700

screen = pygame.display.set_mode((WIDTH , HEIGHT))

pygame.display.set_caption("Cursor Snake Animation")

clock = pygame.time.Clock()

BG = (5, 5 ,20)
HEAD_COLOR = (0 , 255 , 180)
BODY_COLOR = (0 , 180 , 255)
GLOW = (0 , 255 , 255)
snake = []
segments = 25
spacing = 15

x , y = WIDTH // 2, HEIGHT // 2

for i in range(segments):
    snake.append([x - i  * spacing, y])

running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    mx , my = pygame.mouse.get_pos()

    dx = mx - snake[0][0]
    dy = my - snake[0][1]

    angle = math.atan2(dy , dx)

    speed  = 8

    snake [0][0] += math.cos
    (angle) * speed
    snake [0][1] += math.sin
    (angle) * speed

    for i in range (1 , len(snake)):
        prev_x, prev_y = snake[i - 1]
        curr_x,  curr_y = snake[i]

        dx = prev_x - curr_x
        dy = prev_y - curr_y

        dist = math.hypot(dx , dy)

        if dist > spacing:
            angel = math.atan2(dy, dx)
            snake[i][0] += math.cos
            (angel) * (dist - spacing)
            snake [i][1] += math.sin
            (angel) * (dist - spacing)

    screen.fill(BG)

    for i , segment in enumerate(
        reversed(snake)):
        radius = max(5, 18 - i // 2)

        pygame.draw.circle
        (screen , GLOW , (int(segment[0]), int(segment[1])) , radius + 5)

        pygame.draw.circle
        (screen , color , (int (segment[0]) , int (segment[1])) , radius)
    pygame.display.update()
pygame.quit()