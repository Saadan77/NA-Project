import pygame
from player import Player
from platform import Platform
import random

# Initialize Pygame
pygame.init()

# Set up display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Gravity Jumper")

# Set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up fonts
font = pygame.font.Font(None, 36)

# Set up clock
clock = pygame.time.Clock()

# Create the player
player = Player(screen_width // 2, screen_height // 2)

# Generate platforms in a structured manner
def generate_platforms():
    platforms = []
    platform_height = 20
    platform_width = 200
    gap = 100  # Vertical gap between platforms
    num_of_platforms = 6  # Number of platforms

    # Start platform near the bottom of the screen
    start_y = screen_height - 100  # Start from the bottom

    for i in range(num_of_platforms):
        x = random.randint(50, screen_width - platform_width - 50)  # Horizontal position
        y = start_y - (i * gap)  # Vertical position with gap between platforms
        platform = Platform(x, y, platform_width, platform_height)
        platforms.append(platform)

    return platforms

platforms = generate_platforms()

# Game loop
running = True
score = 0  # Initialize score
previously_on_ground = False  # To track if the player was previously on the ground
while running:
    dt = clock.tick(60) / 1000  # Amount of seconds between each loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update player and check platform collisions
    player.update(dt, platforms)
    
    # Check if player has landed on a platform to increment score
    on_ground = False  # Track whether the player is on the ground this frame
    for platform in platforms:
        if player.y + player.height <= platform.y and player.y + player.height + player.velocity_y >= platform.y:
            if player.x + player.width > platform.x and player.x < platform.x + platform.width:
                on_ground = True
                if not previously_on_ground:  # Increment score only the first time landing on a platform
                    score += 1
                    previously_on_ground = True
                break

    # If player leaves the platform, reset the flag
    if not on_ground:
        previously_on_ground = False

    # Draw
    screen.fill(WHITE)  # Clear the screen
    player.draw(screen)
    for platform in platforms:
        platform.draw(screen)

    # Draw the score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    pygame.display.update()

# Quit Pygame
pygame.quit()
