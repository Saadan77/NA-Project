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
RED = (255, 0, 0)

# Set up fonts
font = pygame.font.Font(None, 36)

# Set up clock
clock = pygame.time.Clock()

# Create the player
player = Player(screen_width // 2, screen_height // 2)

# Game parameters
player_health = 3
game_time = 30  # Game timer set to 30 seconds

def generate_platforms():
    platforms = []
    for _ in range(5):  # Generate 5 platforms
        platform_width = random.randint(100, 200)
        platform_height = 20
        x = random.randint(50, screen_width - platform_width - 50)  # Ensure platform is within screen bounds
        y = random.randint(100, screen_height - 100)  # Platform should not be at the very top or bottom
        platform = Platform(x, y, platform_width, platform_height)  # No more move_direction argument
        platforms.append(platform)
    return platforms

# Function to reset the game
def reset_game():
    global player, platforms, player_health, game_time
    player = Player(screen_width // 2, screen_height // 2)
    platforms = generate_platforms()
    player_health = 3
    game_time = 30

# Generate initial platforms
platforms = generate_platforms()

# Game loop
running = True
score = 0
previously_on_ground = False
game_over = False

while running:
    dt = clock.tick(60) / 1000  # Amount of seconds between each loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if game_over and event.key == pygame.K_r:
                game_over = False
                reset_game()

            if event.key == pygame.K_UP and player.on_ground:
                player.velocity_y = -15  # Jump force

    if not game_over:
        # Update game timer
        game_time -= dt
        if game_time <= 0:
            game_time = 0
            game_over = True

        # Update player and check platform collisions
        player.update(dt, platforms)

        # Check if player has fallen off the screen (Game Over condition)
        if player.y > screen_height:
            player_health -= 1
            if player_health <= 0:
                game_over = True
            else:
                # Reset player position if health is remaining
                player.x = screen_width // 2
                player.y = screen_height // 2

        # Check if player has landed on a platform to increment score
        on_ground = False
        for platform in platforms:
            if player.y + player.height <= platform.y and player.y + player.height + player.velocity_y >= platform.y:
                if player.x + player.width > platform.x and player.x < platform.x + platform.width:
                    on_ground = True
                    if not previously_on_ground:
                        score += 1
                        previously_on_ground = True
                    break

        if not on_ground:
            previously_on_ground = False

        # Update moving platforms
        for platform in platforms:
            platform.update(dt)

        # Draw
        screen.fill(WHITE)  # Clear the screen
        player.draw(screen)
        for platform in platforms:
            platform.draw(screen)

        # Draw the score and health
        score_text = font.render(f"Score: {score}", True, BLACK)
        health_text = font.render(f"Health: {player_health}", True, BLACK)
        time_text = font.render(f"Time: {int(game_time)}", True, BLACK)
        screen.blit(score_text, (10, 10))
        screen.blit(health_text, (10, 40))
        screen.blit(time_text, (10, 70))

    else:
        # Game Over Screen
        game_over_text = font.render("Game Over! Press 'R' to Restart", True, RED)
        screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2))

    pygame.display.update()

# Quit Pygame
pygame.quit()
