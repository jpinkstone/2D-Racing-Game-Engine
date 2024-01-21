import pygame
import pygame_gui
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
pygame.display.set_caption("Top-Down Racing Game")
clock = pygame.time.Clock()

# Pygame GUI
manager = pygame_gui.UIManager((WIDTH, HEIGHT))

# Player car
player_size = 50
player_x = WIDTH // 2 - player_size // 2
player_y = HEIGHT - 100
player_speed = 1
player_max_speed = 5  # Increased max speed
acceleration = 1.0  # Increased acceleration
deceleration_factor = 0.2
player_velocity = [0, 0]
player_angle = 0  # Initial angle in degrees

# Load race car image
race_car_image = pygame.image.load("race_car.png")  # Replace "race_car.png" with the actual filename of your race car image
race_car_image = pygame.transform.scale(race_car_image, (player_size, player_size))

# Track
track_width = 100
track_points = [(WIDTH // 4, HEIGHT // 4),
                (WIDTH // 4 + WIDTH // 2, HEIGHT // 4),
                (WIDTH // 4 + WIDTH // 2, HEIGHT // 4 + HEIGHT // 2),
                (WIDTH // 4, HEIGHT // 4 + HEIGHT // 2)]
track_rect = pygame.Rect((WIDTH // 4, HEIGHT // 4, WIDTH // 2, HEIGHT // 2))

# GUI elements
track_points_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((10, 10), (200, 30)),
                                                 text='Track Points:')
track_points_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((210, 10), (150, 30)),
                                                         manager=manager)

# Function to rotate an image
def rotate_image(image, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    return rotated_image

# Game loop
accelerating = False  # Flag to track if accelerating
decelerating = False  # Flag to track if decelerating
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                accelerating = True
            elif event.key == pygame.K_DOWN:
                decelerating = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                accelerating = False
            elif event.key == pygame.K_DOWN:
                decelerating = False
        manager.process_events(event)

    # Update Pygame GUI
    manager.update(FPS / 1000.0)

    # Player movement
    keys = pygame.key.get_pressed()
    player_velocity[0] = 0
    player_velocity[1] = 0
    if keys[pygame.K_LEFT]:
        player_angle += 5  # Rotate left
    if keys[pygame.K_RIGHT]:
        player_angle -= 5  # Rotate right

    # Acceleration
    if accelerating:
        player_speed += acceleration
        player_speed = min(player_speed, player_max_speed)
    elif decelerating:
        player_speed -= deceleration_factor
        player_speed = max(player_speed, 0)

    # Update player position and rotation
    player_velocity[0] = player_speed * pygame.math.Vector2(1, 0).rotate(-player_angle).x
    player_velocity[1] = player_speed * pygame.math.Vector2(1, 0).rotate(-player_angle).y
    player_x += player_velocity[0]
    player_y += player_velocity[1]
    rotated_car_image = rotate_image(race_car_image, player_angle)

    # Check for collision with the track box
    if not track_rect.collidepoint(player_x + player_size // 2, player_y + player_size // 2):
        # Simple bounce off the track
        player_velocity[0] = -player_velocity[0]
        player_velocity[1] = -player_velocity[1]

    # Update track points from GUI input
    try:
        track_points_input_str = track_points_input.get_text().replace('(', '').replace(')', '')
        track_points = [tuple(map(int, point.split(','))) for point in track_points_input_str.split(';')]
        track_rect = pygame.Rect(*track_points[0], track_points[2][0] - track_points[0][0], track_points[2][1] - track_points[0][1])
    except ValueError:
        pass  # Ignore invalid input

    # Update game state

    # Draw background
    screen.fill(WHITE)

    # Draw track
    pygame.draw.polygon(screen, GRAY, track_points, 2)

    # Draw rotated player car
    screen.blit(rotated_car_image, (player_x, player_y))

    # Draw GUI
    manager.draw_ui(screen)

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit the game
pygame.quit()
sys.exit()
