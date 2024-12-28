import pygame
from player import Player
from platform import Platform # type: ignore
import random
from utils import trapezoidal_rule, linear_regression
from obstacle import Obstacle

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
player = Player(screen_width // 2, screen_height - 120)

# Game parameters
player_health = 3
game_time = 30  # Game timer set to 30 seconds
level = 1
score = 0

# Add obstacles to the game
obstacles = []
obstacle_base_speed = 50
obstacle_count = 3  # Adjust dynamically

# Difficulty adjustment factors for linear regression
difficulty_slope = 0.05  # Increase difficulty gradually with score
difficulty_intercept = 1.0  # Base difficulty level

# Function to generate new obstacles
# Example of creating lists for trapezoidal_rule
def generate_obstacles(level, difficulty_factor):
    obstacle_list = []
    for i in range(obstacle_count):
        width = 50
        height = 30
        x = random.randint(50, screen_width - width - 50)
        y = random.randint(-200, -50)
        
        # Adjust this section based on trapezoidal rule
        # For example, you could integrate between level 0 and the current level:
        x_values = [0, level]  # Just a simple example for x-values (level as a representation)
        y_values = [difficulty_factor, difficulty_factor + 0.5]  # Adjust this based on your logic
        speed = trapezoidal_rule(x_values, y_values)  # Call with correct arguments
        
        obstacle = Obstacle(x, y, width, height, speed)
        obstacle_list.append(obstacle)
    return obstacle_list

# Add initial obstacles
obstacles = generate_obstacles(level, linear_regression(score, difficulty_slope, difficulty_intercept))

# Generate platforms with more even distribution
def generate_platforms(level):
    platforms = []
    platform_count = 5 + level  # Number of platforms increases with level
    spacing = screen_height // (platform_count + 1)  # Distribute platforms evenly in vertical space

    for i in range(platform_count):
        platform_width = random.randint(100, 150)
        platform_height = 20
        x = random.randint(50, screen_width - platform_width - 50)  # Random horizontal position
        y = spacing * (i + 1) + random.randint(-20, 20)  # Small random offset for variety
        platform_type = random.choice(["normal", "moving", "disappearing", "bouncy"])
        platform = Platform(x, y, platform_width, platform_height, platform_type)
        platforms.append(platform)

    return platforms

# Reset game state
def reset_game():
    global player, platforms, player_health, game_time, level, score
    player = Player(screen_width // 2, screen_height - 120)
    platforms = generate_platforms(level)
    static_platform = Platform(screen_width // 2 - 100, screen_height - 40, 200, 20)  # Smaller static platform
    platforms.insert(0, static_platform)
    player_health = 3
    game_time = 30
    level = 1
    score = 0

# Draw health bar
def draw_health_bar(screen, x, y, health, max_health):
    bar_width = 200
    bar_height = 20
    fill = (health / max_health) * bar_width
    pygame.draw.rect(screen, RED, (x, y, bar_width, bar_height))
    pygame.draw.rect(screen, (0, 255, 0), (x, y, fill, bar_height))

# Generate initial platforms and add the static platform
platforms = generate_platforms(level)
static_platform = Platform(screen_width // 2 - 100, screen_height - 40, 200, 20)  # Smaller static platform
platforms.insert(0, static_platform)

# Game loop
running = True
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
            if player_health <= 0:  # If health is 0 or below, game over
                player_health = 0  # Ensure health does not go below 0
                game_over = True
            else:
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
        for platform in platforms:  # <-- Place this here
            platform.update(dt)
        
        # Update difficulty factor dynamically
        difficulty_factor = linear_regression(score, difficulty_slope, difficulty_intercept)

        # Update obstacles
        for obstacle in obstacles:
            obstacle.update(dt)

            # Check for collision with obstacles (decrease health if collided)
            for obstacle in obstacles:
                if (player.x < obstacle.x + obstacle.width and 
                    player.x + player.width > obstacle.x and 
                    player.y < obstacle.y + obstacle.height and 
                    player.y + player.height > obstacle.y):
                    
                    player_health -= 1
                    
                    if player_health <= 0:  # Game Over when health reaches zero
                        player_health = 0
                        game_over = True
                    else:
                        obstacles.remove(obstacle)

        # Add new obstacles periodically or based on levels
        if len(obstacles) < 3:  # Maintain a set number of obstacles
            x = random.randint(50, screen_width - 100)
            speed = random.randint(50, 150)
            obstacles.append(Obstacle(x, -50, 50, 50, speed))

        # Increase level difficulty based on score
        if score >= level * 10:
            level += 1
            platforms = generate_platforms(level)
            obstacles = generate_obstacles(level, difficulty_factor)

        # Draw
        screen.fill(WHITE)
        player.draw(screen)
        for platform in platforms:
            platform.draw(screen)
        for obstacle in obstacles:
            obstacle.draw(screen)

        # Draw the score, health, time, and level
        score_text = font.render(f"Score: {score}", True, BLACK)
        health_text = font.render(f"Health: {player_health}", True, BLACK)
        time_text = font.render(f"Time: {int(game_time)}", True, BLACK)
        level_text = font.render(f"Level: {level}", True, BLACK)
        difficulty_text = font.render(f"Difficulty: {difficulty_factor:.2f}", True, BLACK)
        screen.blit(score_text, (10, 10))
        screen.blit(health_text, (10, 40))
        screen.blit(time_text, (10, 70))
        screen.blit(level_text, (10, 100))
        screen.blit(difficulty_text, (10, 130))
        draw_health_bar(screen, 550, 10, player_health, 3)

    else:
        # Game Over Screen
        game_over_text = font.render("Game Over! Press 'R' to Restart", True, RED)
        screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2))

    pygame.display.update()

# Quit Pygame
pygame.quit()
