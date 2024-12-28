import pygame
from utils import trapezoidal_rule

class Obstacle:
    def __init__(self, x, y, width, height, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.positions = [(0, y)]  # Store (time, y-position) tuples

    def update(self, dt):
        # Update y position
        self.y += self.speed * dt
        current_time = self.positions[-1][0] + dt
        self.positions.append((current_time, self.y))

        # Limit stored positions to avoid memory overflow
        if len(self.positions) > 100:
            self.positions.pop(0)

    def distance_traveled(self):
        # Extract time (x) and positions (y) from self.positions
        times = [pos[0] for pos in self.positions]
        y_values = [pos[1] for pos in self.positions]

        # Use Trapezoidal Rule for distance calculation
        return trapezoidal_rule(times, y_values)

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height))
