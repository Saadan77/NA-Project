import pygame
from utils import bisection_method  # Import bisection_method from utils.py

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

    def collision_func(self, t, player):
        """
        A helper function for collision detection.
        We want to find the point where the player and the obstacle intersect.
        Returns a positive value if no collision; negative if a collision is about to occur.
        """
        player_bottom = player.y + player.height
        obstacle_bottom = self.y + self.height

        # Check for vertical intersection: the player and obstacle are in the same y-range
        if player.x + player.width > self.x and player.x < self.x + self.width:
            return player_bottom - obstacle_bottom  # Difference between player bottom and obstacle bottom
        return float('inf')  # No collision if no x-overlap

    def distance_to_collision(self, player, tol=1e-5):
        """
        Uses the Bisection method to estimate when a collision with an obstacle will happen.
        """
        def func_to_solve(t):
            return self.collision_func(t, player)
        
        # Time of collision estimation using bisection
        try:
            return bisection_method(func_to_solve, 0, 1, tol)  # Adjust bounds as necessary
        except ValueError:
            return None  # No collision (could add more logic)

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height))
