import pygame
import math
import sys

# --- Constants & Designer Palette ---
WIDTH, HEIGHT = 1000, 750
FPS = 60
# Colors
CLR_ASPHALT = (33, 37, 41)
CLR_WALL    = (73, 80, 87)
CLR_CAR     = (230, 57, 70)
CLR_SPOT    = (168, 218, 220)
CLR_TEXT    = (241, 250, 238)
CLR_HUD     = (29, 53, 87)

class Car:
    def __init__(self, x, y, angle=0):
        self.x, self.y = float(x), float(y)
        self.angle = angle
        self.speed = 0
        self.max_speed = 4.5
        self.accel = 0.12
        self.friction = 0.94
        self.steer_sense = 3.5
        self.health = 100
        self.width, self.height = 48, 24

    def get_rect(self):
        # Returns a rect centered on the car for collision
        return pygame.Rect(self.x - self.width//2, self.y - self.height//2, self.width, self.height)

    def update(self, keys, walls):
        # Movement input
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.speed += self.accel
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.speed -= self.accel
        else:
            self.speed *= self.friction

        # Speed Limiting
        self.speed = max(-self.max_speed/2, min(self.speed, self.max_speed))

        # Steering (Relative to speed)
        if abs(self.speed) > 0.1:
            direction = 1 if self.speed > 0 else -1
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.angle += self.steer_sense * direction
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.angle -= self.steer_sense * direction

        # Apply Physics
        old_x, old_y = self.x, self.y
        self.x += math.cos(math.radians(self.angle)) * self.speed
        self.y -= math.sin(math.radians(self.angle)) * self.speed

        # Collision with Walls
        current_rect = self.get_rect()
        for wall in walls:
            if current_rect.colliderect(wall):
                self.health -= 10
                self.speed = -self.speed * 0.5 # Bounce
                self.x, self.y = old_x, old_y # Revert move

    def draw(self, screen):
        # Create a surface for the car to rotate it properly
        car_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        # Designer Car Body
        pygame.draw.rect(car_surface, CLR_CAR, (0, 0, self.width, self.height), border_radius=5)
        # Windows
        pygame.draw.rect(car_surface, (200, 230, 255), (30, 4, 12, 16), border_radius=2)
        # Lights
        pygame.draw.circle(car_surface, (255, 255, 200), (44, 6), 3)
        pygame.draw.circle(car_surface, (255, 255, 200), (44, 18), 3)

        rotated_car = pygame.transform.rotate(car_surface, self.angle)
        new_rect = rotated_car.get_rect(center=(self.x, self.y))
        screen.blit(rotated_car, new_rect)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Extreme Precision Parking")
        self.clock = pygame.time.Clock()
        self.font_main = pygame.font.SysFont("Segoe UI", 28, bold=True)
        self.font_logo = pygame.font.SysFont("Impact", 60)
        self.level = 0
        self.setup_level()

    def setup_level(self):
        # Define Levels: (SpawnX, SpawnY, TargetRect, WallList)
        levels = [
            # Level 1: Straight Shot
            (100, 375, pygame.Rect(850, 325, 80, 100), [
                pygame.Rect(400, 0, 40, 300), pygame.Rect(400, 450, 40, 300)
            ]),
            # Level 2: The S-Curve
            (100, 100, pygame.Rect(800, 600, 100, 80), [
                pygame.Rect(0, 250, 700, 40), pygame.Rect(300, 500, 700, 40)
            ]),
            # Level 3: The Box
            (500, 375, pygame.Rect(50, 50, 80, 80), [
                pygame.Rect(200, 200, 600, 20), pygame.Rect(200, 550, 600, 20),
                pygame.Rect(200, 200, 20, 370), pygame.Rect(780, 200, 20, 370)
            ])
        ]
        
        if self.level < len(levels):
            l = levels[self.level]
            self.car = Car(l[0], l[1])
            self.target = l[2]
            self.walls = l[3]
            # Add screen boundaries as walls
            self.walls.extend([
                pygame.Rect(0, 0, WIDTH, 10), pygame.Rect(0, HEIGHT-10, WIDTH, 10),
                pygame.Rect(0, 0, 10, HEIGHT), pygame.Rect(WIDTH-10, 0, 10, HEIGHT)
            ])
            self.won_level = False
        else:
            self.all_cleared = True

    def draw_hud(self):
        # Top Panel
        pygame.draw.rect(self.screen, CLR_HUD, (0, 0, WIDTH, 60))
        lvl_txt = self.font_main.render(f"LEVEL: {self.level + 1}", True, CLR_TEXT)
        hp_txt = self.font_main.render(f"HEALTH: {self.car.health}%", True, (46, 204, 113) if self.car.health > 40 else (231, 76, 60))
        self.screen.blit(lvl_txt, (20, 12))
        self.screen.blit(hp_txt, (WIDTH - 220, 12))

    def run(self):
        while True:
            self.screen.fill(CLR_ASPHALT)
            keys = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()

            # Logic
            if self.car.health > 0 and not self.won_level:
                self.car.update(keys, self.walls)

            # Win Condition: Car fully in spot and stopped
            if self.target.contains(self.car.get_rect()) and abs(self.car.speed) < 0.2:
                self.won_level = True

            # Drawing
            # 1. Target Spot
            pygame.draw.rect(self.screen, CLR_SPOT, self.target, 3, border_radius=8)
            overlay = pygame.Surface((self.target.width, self.target.height), pygame.SRCALPHA)
            pygame.draw.rect(overlay, (*CLR_SPOT, 60), (0,0,self.target.width, self.target.height), border_radius=8)
            self.screen.blit(overlay, self.target.topleft)

            # 2. Walls
            for wall in self.walls:
                pygame.draw.rect(self.screen, CLR_WALL, wall)

            # 3. Car
            self.car.draw(self.screen)
            self.draw_hud()

            # Overlays
            if self.car.health <= 0:
                txt = self.font_logo.render("GAME OVER - Press R", True, (255, 50, 50))
                self.screen.blit(txt, (WIDTH//2 - 250, HEIGHT//2))
                if keys[pygame.K_r]: self.setup_level()

            if self.won_level:
                txt = self.font_logo.render("LEVEL COMPLETE! - Press SPACE", True, (50, 255, 100))
                self.screen.blit(txt, (WIDTH//2 - 350, HEIGHT//2))
                if keys[pygame.K_SPACE]:
                    self.level += 1
                    self.setup_level()

            pygame.display.flip()
            self.clock.tick(FPS)

if __name__ == "__main__":
    Game().run()