import pygame # type: ignore

class Platform:
    def __init__(self, x, y, width, height, platform_type="normal"):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.type = platform_type
        self.color = (0, 255, 0)
        self.move_speed = 0  # Default move speed for non-moving platforms

        if platform_type == "moving":
            self.move_speed = 2  # Set a speed for moving platforms
        elif platform_type == "bouncy":
            self.color = (0, 0, 255)
        elif platform_type == "disappearing":
            self.color = (255, 0, 0)

    def update(self, dt):
        if self.type == "moving":
            self.x += self.move_speed  # Update platform position
            if self.x <= 50 or self.x >= 750 - self.width:
                self.move_speed = -self.move_speed  # Reverse direction at boundaries

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
