import pygame
import random
from constants import *
from circleshape import CircleShape

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.velocity = pygame.Vector2(0, 0)
        for group in getattr(Asteroid, "containers", []):
            group.add(self)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, 2)

    def update(self, dt):
        self.position += self.velocity * dt

    def split(self):
        # Kill this asteroid (remove from all groups)
        self.kill()

        # If radius is small enough, no splitting, just disappear
        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        # Calculate new smaller radius
        new_radius = self.radius - ASTEROID_MIN_RADIUS

        # Generate a random angle between 20 and 50 degrees
        random_angle = random.uniform(20, 50)

        # Create two new velocities by rotating current velocity
        velocity1 = self.velocity.rotate(random_angle) * 1.2
        velocity2 = self.velocity.rotate(-random_angle) * 1.2

        # Spawn two new smaller asteroids with new radius and velocities
        asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid1.velocity = velocity1

        asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid2.velocity = velocity2
