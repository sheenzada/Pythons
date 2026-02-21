import pygame
import math
import sys

# --- CONFIGURATION ---
WIDTH, HEIGHT = 1000, 750
FPS = 60
CAR_WIDTH, CAR_HEIGHT = 50, 26

# Colors
ASPHALT = (28, 28, 30)
GRASS = (39, 174, 96)
WALL = (52, 73, 94)
ACCENT = (231, 76, 60)
UI_BG = (44, 62, 80, 180)

class GameState:
    def __init__(self):
        self.level = 1
        self.score = 0
        self.health = 100
        self.game_over = False
        self.win = False

class Car:
    def __init__(self, x, y, angle=0):
        self.x, self.y = float(x), float(y)
        self.angle = angle
        self.speed = 0
        self.max_speed = 5.0
        self.accel = 0.15
        self.friction = 0.94
        self.steer_angle = 0
        self.health = 100

    def update(self, keys, walls):
        if self.health <= 0: return

        # Movement Logic
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.speed += self.accel
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.speed -= self.accel
        else:
            self.speed *= self.friction

        # Drift/Steering logic
        if abs(self.speed) > 0.1:
            steer_limit = 4.0
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.angle += steer_limit * (self.speed / self.max_speed)
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.angle -= steer_limit * (self.speed / self.max_speed)

        # Physics calculation
        old_x, old_y = self.x, self.y
        self.x += math.cos(math.radians(self.angle)) * self.speed
        self.y -= math.sin(math.radians(self.angle)) * self.speed

        # Precise Collision Mask
        car_rect = pygame.Rect(self.x - 25, self.y - 13, 50, 26)
        for wall in walls:
            if car_rect.colliderect(wall):
                self.health -= 5 # Damage on hit
                self.speed = -self.speed * 0.6 # Bounce
                self.x, self.y = old_x, old_y

    def draw(self, surface):
        car_surf = pygame.Surface((50, 26), pygame.SRCALPHA)
        # Gradient Body
        body_color = (231, 76, 60) if self.health > 30 else (100, 30, 30)
        pygame.draw.rect(car_surf, body_color, (0, 0, 50, 26), border_radius=6)
        # Detail lines
        pygame.draw.rect(car_surf, (44, 62, 80), (32, 4, 12, 18), border_radius=2) # Windshield
        pygame.draw.circle(car_surf, (255, 255, 255), (46, 6), 3) # Headlight
        pygame.draw.circle(car_surf, (255, 255, 255), (46, 20), 3)

        rotated = pygame.transform.rotate(car_surf, self.angle)
        rect = rotated.get_rect(center=(self.x, self.y))
        surface.blit(rotated, rect)

def draw_ui(screen, state, car):
    # Top Bar
    ui_surf = pygame.Surface((WIDTH, 60), pygame.SRCALPHA)
    ui_surf.fill(UI_BG)
    screen.blit(ui_surf, (0, 0))
    
    font = pygame.font.SysFont("Verdana", 22, bold=True)
    lvl_txt = font.render(f"LEVEL: {state.level}", True, (255, 255, 255))
    hp_txt = font.render(f"CAR HEALTH: {int(car.health)}%", True, (46, 204, 113) if car.health > 50 else (231, 76, 60))
    
    screen.blit(lvl_txt, (30, 15))
    screen.blit(hp_txt, (WIDTH - 250, 15))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    state = GameState()
    
    # LEVEL DESIGN
    levels = [
        {
            "spawn": (100, 100),
            "target": pygame.Rect(800, 600, 70, 110),
            "walls": [pygame.Rect(400, 0, 50, 500), pygame.Rect(0, 730, 1000, 20)]
        },
        {
            "spawn": (100, 600),
            "target": pygame.Rect(850, 100, 70, 110),
            "walls": [pygame.Rect(300, 200, 400, 40), pygame.Rect(300, 500, 400, 40)]
        }
    ]

    current_lvl_idx = 0
    lvl_data = levels[current_lvl_idx]
    car = Car(*lvl_data["spawn"])

    while True:
        screen.fill(ASPHALT)
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Update
        if car.health > 0 and not state.win:
            car.update(keys, lvl_data["walls"])

        # Check Parking Win
        car_rect = pygame.Rect(car.x-25, car.y-13, 50, 26)
        if lvl_data["target"].contains(car_rect) and abs(car.speed) < 0.2:
            current_lvl_idx += 1
            if current_lvl_idx < len(levels):
                lvl_data = levels[current_lvl_idx]
                car = Car(*lvl_data["spawn"])
                state.level += 1
            else:
                state.win = True

        # Draw Environment
        pygame.draw.rect(screen, (241, 196, 15, 150), lvl_data["target"], 3, border_radius=5)
        for w in lvl_data["walls"]:
            pygame.draw.rect(screen, WALL, w)
            pygame.draw.rect(screen, (0,0,0), w, 2) # Wall border

        car.draw(screen)
        draw_ui(screen, state, car)

        if car.health <= 0:
            msg = pygame.font.SysFont("Impact", 80).render("TOTALED!", True, (255, 0, 0))
            screen.blit(msg, (WIDTH//2 - 150, HEIGHT//2 - 50))
        
        if state.win:
            msg = pygame.font.SysFont("Impact", 80).render("PRO PARKER!", True, (46, 204, 113))
            screen.blit(msg, (WIDTH//2 - 200, HEIGHT//2 - 50))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()