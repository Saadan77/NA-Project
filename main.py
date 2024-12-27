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
while running:
    dt = clock.tick(60) / 1000  # Amount of seconds between each loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update
    player.update(dt, platforms)

    # Draw
    screen.fill(WHITE)  # Clear the screen
    player.draw(screen)
    for platform in platforms:
        platform.draw(screen)

    pygame.display.update()

# Quit Pygame
pygame.quit()
