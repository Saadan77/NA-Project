import pygame # type: ignore
import random

class Platform:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = (0, 255, 0)  # Green color for platforms
        self.move_speed = random.randint(1, 3)  # Speed of horizontal movement
        self.initial_x = x  # Store initial X position for horizontal movement

    def update(self, dt):
        # Horizontal movement logic
        self.x += self.move_speed * dt
        if self.x <= 50 or self.x >= 600:
            self.move_speed = -self.move_speed  # Reverse direction if platform hits screen edges

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
