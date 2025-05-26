import pygame
from circleshape import CircleShape  # Adjust import if needed
from constants import SHOT_RADIUS

class Shot(CircleShape, pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self, self.containers)
        CircleShape.__init__(self, x, y, SHOT_RADIUS)
        self.velocity = pygame.Vector2(0, 0)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius)

    def update(self, dt):
        self.position += self.velocity * dt

        # Optional: remove the shot if it goes off screen to save resources
        if (
            self.position.x < 0
            or self.position.x > 800  # Use SCREEN_WIDTH if imported
            or self.position.y < 0
            or self.position.y > 600  # Use SCREEN_HEIGHT if imported
        ):
            self.kill()
