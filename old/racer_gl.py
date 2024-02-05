# Game physics prototype
import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
GRAY = (169, 169, 169)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tiny Turismo")
clock = pygame.time.Clock()

class Car:
    def __init__(self):
        self.size = 50
        self.x = WIDTH // 2 - self.size // 2
        self.y = HEIGHT - 100
        self.speed = 1
        self.max_speed = 5
        self.acceleration = 1.0
        self.deceleration_factor = 0.2
        self.velocity = [0, 0]
        self.angle = 0
        self.accelerating = False
        self.decelerating = False

    def rot_center(self, image, angle):
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

    def accelerate(self):
        self.speed += self.acceleration
        self.speed = min(self.speed, self.max_speed)

    def decelerate(self):
        self.speed -= self.deceleration_factor
        self.speed = max(self.speed, 0)
    # def drift(self, keys):
    #     if (keys[pygame.K_SPACE] and keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]) or (self.speed > 6 and keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]) and not keys[pygame.K_DOWN]:
    #         print("Drifting")
    #         if keys[pygame.K_a] and self.drift_distance < 50:
    #             self.drift_distance += 1
    #         elif keys[pygame.K_d] and self.drift_distance > -50:
    #             self.drift_distance -= 1
    #     else:
    #         if self.drift_distance > 0:
    #             self.drift_distance -= 1
    #             if self.speed > 1:
    #                 self.speed -= 0.1
    #             if self.drift_distance < 0:
    #                 self.drift_distance = 0
    #         elif self.drift_distance < 0:
    #             self.drift_distance += 1
    #             if self.speed > 1:
    #                 self.speed -= 0.1

    #             if self.drift_distance > 0:
    #                 self.drift_distance = 0

car = Car()

# Load race car image
race_car_image = pygame.image.load("./assets/race_car.png") 
race_car_image = pygame.transform.scale(race_car_image, (car.size, car.size))

# Track
track_width = 100
track_points = [(WIDTH // 4, HEIGHT // 4),
                (WIDTH // 4 + WIDTH // 2, HEIGHT // 4),
                (WIDTH // 4 + WIDTH // 2, HEIGHT // 4 + HEIGHT // 2),
                (WIDTH // 4, HEIGHT // 4 + HEIGHT // 2)]
track_rect = pygame.Rect((WIDTH // 4, HEIGHT // 4, WIDTH // 2, HEIGHT // 2))

# Game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                car.accelerating = True
            elif event.key == pygame.K_DOWN:
                car.decelerating = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                car.accelerating = False
            elif event.key == pygame.K_DOWN:
                car.decelerating = False

    # Player movement
    keys = pygame.key.get_pressed()
    car.velocity[0] = 0
    car.velocity[1] = 0
    if keys[pygame.K_LEFT]:
        car.angle += 5  # Rotate left
    if keys[pygame.K_RIGHT]:
        car.angle -= 5  # Rotate right

    # Acceleration
    if car.accelerating:
        car.accelerate()
    elif car.decelerating:
        car.decelerate()

    # car.drift(keys)
    
    # Update player position and rotation
    car.velocity[0] = car.speed * pygame.math.Vector2(1, 0).rotate(-car.angle).x
    car.velocity[1] = car.speed * pygame.math.Vector2(1, 0).rotate(-car.angle).y
    car.x += car.velocity[0]
    car.y += car.velocity[1]

    rotated_car_image = car.rot_center(race_car_image, car.angle)

    # Check for collision with the track box
    if not track_rect.collidepoint(car.x + car.size // 2, car.y + car.size // 2):
        # Adjust position to be inside the track
        car.x = max(min(car.x, track_rect.right - car.size), track_rect.left)
        car.y = max(min(car.y, track_rect.bottom - car.size), track_rect.top)
        # Simple bounce off the track
        car.velocity[0] = -car.velocity[0]
        car.velocity[1] = -car.velocity[1]

    # Draw background
    screen.fill(WHITE)

    # Draw track
    pygame.draw.polygon(screen, GRAY, track_points, 2)

    # Draw rotated player car
    screen.blit(rotated_car_image, (car.x, car.y))

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit the game
pygame.quit()
sys.exit()
