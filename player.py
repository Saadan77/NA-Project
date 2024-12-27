import pygame

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.color = (0, 0, 255)  # Blue color
        self.velocity_x = 0
        self.velocity_y = 0
        self.speed = 5
        self.gravity = 0.5
        self.on_ground = False

    def update(self, dt, platforms):
        # Handle movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.velocity_x = -self.speed
        elif keys[pygame.K_RIGHT]:
            self.velocity_x = self.speed
        else:
            self.velocity_x = 0

        self.x += self.velocity_x

        # Apply gravity
        if not self.on_ground:
            self.velocity_y += self.gravity
        self.y += self.velocity_y

        # Check collision with platforms
        self.on_ground = False
        for platform in platforms:
            # Check if the player is falling onto the platform
            if self.y + self.height <= platform.y and self.y + self.height + self.velocity_y >= platform.y:
                if self.x + self.width > platform.x and self.x < platform.x + platform.width:
                    # Adjust player position to land on the platform
                    self.velocity_y = 0
                    self.y = platform.y - self.height  # Place player just above the platform
                    self.on_ground = True
                    break

        # Keep player within bounds
        if self.x < 0:
            self.x = 0
        elif self.x + self.width > 800:
            self.x = 800 - self.width

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
