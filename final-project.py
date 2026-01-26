import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import random
import math

# ==================================================
# CONFIGURATION
# ==================================================
WIDTH = 12
HEIGHT = 25

LANES = [3, 5, 7, 9]
ROAD_LEFT = 2
ROAD_RIGHT = 10

MAX_SPEED = 0.6
ACCELERATION = 0.01
BRAKE_FORCE = 0.03
FUEL_CONSUMPTION = 0.02

FPS = 80

# ==================================================
# TRUCK MODEL
# ==================================================
class Truck:
    def __init__(self):
        self.lane = 1
        self.x = LANES[self.lane]
        self.y = 2

        self.width = 1
        self.height = 2

        self.speed = 0.2
        self.health = 100
        self.fuel = 100

    def move_left(self):
        if self.lane > 0:
            self.lane -= 1
            self.x = LANES[self.lane]

    def move_right(self):
        if self.lane < len(LANES) - 1:
            self.lane += 1
            self.x = LANES[self.lane]

    def accelerate(self):
        self.speed = min(MAX_SPEED, self.speed + ACCELERATION)

    def brake(self):
        self.speed = max(0.1, self.speed - BRAKE_FORCE)

    def consume_fuel(self):
        self.fuel = max(0, self.fuel - FUEL_CONSUMPTION * self.speed * 10)

    def draw(self, ax):
        ax.add_patch(
            plt.Rectangle((self.x, self.y),
                          self.width, self.height,
                          color="blue")
        )

# ==================================================
# OBSTACLE WITH SIMPLE AI
# ==================================================
class Obstacle:
    def __init__(self, speed):
        self.lane = random.randint(0, len(LANES) - 1)
        self.x = LANES[self.lane]
        self.y = HEIGHT
        self.speed = speed
        self.damage = random.randint(5, 20)

    def update(self):
        self.y -= self.speed

    def draw(self, ax):
        ax.add_patch(
            plt.Rectangle((self.x, self.y),
                          1, 1,
                          color="red")
        )

# ==================================================
# ENVIRONMENT SYSTEM
# ==================================================
class Environment:
    def __init__(self):
        self.time = 0
        self.is_night = False

    def update(self):
        self.time += 1
        self.is_night = (self.time // 300) % 2 == 1

    def background_color(self):
        return "#222244" if self.is_night else "#dddddd"

# ==================================================
# GAME ENGINE
# ==================================================
class TruckSimulation:
    def __init__(self):
        self.truck = Truck()
        self.obstacles = []
        self.env = Environment()

        self.score = 0
        self.level = 1
        self.paused = False
        self.game_over = False

        self.fig, self.ax = plt.subplots(figsize=(5, 9))
        plt.close()

        self.fig.canvas.mpl_connect("key_press_event", self.key_down)

    # --------------------------
    # INPUT SYSTEM
    # --------------------------
    def key_down(self, event):
        if event.key in ["left", "a"]:
            self.truck.move_left()
        elif event.key in ["right", "d"]:
            self.truck.move_right()
        elif event.key == "up":
            self.truck.accelerate()
        elif event.key == "down":
            self.truck.brake()
        elif event.key == "p":
            self.paused = not self.paused

    # --------------------------
    # SPAWN SYSTEM
    # --------------------------
    def spawn_obstacle(self):
        probability = min(0.15, 0.05 + self.level * 0.01)
        if random.random() < probability:
            self.obstacles.append(
                Obstacle(self.truck.speed + 0.1)
            )

    # --------------------------
    # COLLISION SYSTEM
    # --------------------------
    def collision_check(self):
        for obs in self.obstacles:
            if (
                obs.lane == self.truck.lane and
                obs.y <= self.truck.y + 1
            ):
                self.truck.health -= obs.damage
                self.obstacles.remove(obs)

    # --------------------------
    # LEVEL SYSTEM
    # --------------------------
    def level_update(self):
        self.level = 1 + self.score // 500

    # --------------------------
    # DRAWING
    # --------------------------
    def draw_road(self):
        for lane in LANES:
            self.ax.axvline(lane - 0.5, color="white", linestyle="--", alpha=0.3)

        self.ax.axvline(ROAD_LEFT, color="black", linewidth=3)
        self.ax.axvline(ROAD_RIGHT, color="black", linewidth=3)

    def draw_ui(self):
        self.ax.text(0.3, 24, f"Score: {self.score}", fontsize=9)
        self.ax.text(0.3, 23, f"Level: {self.level}", fontsize=9)
        self.ax.text(0.3, 22, f"Speed: {self.truck.speed:.2f}", fontsize=9)
        self.ax.text(0.3, 21, f"Fuel: {int(self.truck.fuel)}%", fontsize=9)
        self.ax.text(0.3, 20, f"Health: {self.truck.health}", fontsize=9)

        if self.paused:
            self.ax.text(4, 13, "PAUSED", fontsize=20)

    # --------------------------
    # MAIN LOOP
    # --------------------------
    def update(self, frame):
        if self.game_over:
            self.ax.text(3, 13, "GAME OVER", fontsize=22)
            self.ax.text(3, 11, f"Final Score: {self.score}", fontsize=12)
            return

        if self.paused:
            return

        self.ax.clear()
        self.ax.set_xlim(0, WIDTH)
        self.ax.set_ylim(0, HEIGHT)
        self.ax.set_xticks([])
        self.ax.set_yticks([])

        # Environment
        self.env.update()
        self.ax.set_facecolor(self.env.background_color())

        # Systems update
        self.spawn_obstacle()
        self.truck.consume_fuel()
        self.level_update()

        for obs in self.obstacles:
            obs.update()

        self.collision_check()
        self.obstacles = [o for o in self.obstacles if o.y > 0]

        # Draw
        self.draw_road()
        self.truck.draw(self.ax)

        for obs in self.obstacles:
            obs.draw(self.ax)

        self.draw_ui()

        # Score logic
        self.score += int(self.truck.speed * 10)

        # End conditions
        if self.truck.health <= 0 or self.truck.fuel <= 0:
            self.game_over = True

    # --------------------------
    # RUN
    # --------------------------
    def run(self):
        self.anim = animation.FuncAnimation(
            self.fig, self.update, interval=FPS
        )
        return self.anim


# ==================================================
# START SIMULATION
# ==================================================
simulation = TruckSimulation()
simulation.run()
