import pygame
from constants import *
from shot import Shot
from constants import PLAYER_SHOOT_SPEED, PLAYER_SHOOT_COOLDOWN, PLAYER_TURN_SPEED, PLAYER_SPEED, PLAYER_RADIUS

class CircleShape:
    def __init__(self, x, y, radius):
        self.position = pygame.Vector2(x, y)
        self.radius = radius

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, 2)

class Player(CircleShape, pygame.sprite.Sprite):
    def __init__(self, x, y):
        CircleShape.__init__(self, x, y, PLAYER_RADIUS)
        pygame.sprite.Sprite.__init__(self)

        self.rotation = 0  # degrees, 0 means facing "up"
        self.shoot_cooldown = 0  # timer for shooting cooldown

        # Automatically add to groups if containers are set
        for group in getattr(Player, "containers", []):
            group.add(self)

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), 2)

    def rotate(self, direction, dt):
        # direction is expected to be +1 (right) or -1 (left)
        self.rotation += PLAYER_TURN_SPEED * dt * direction
        self.rotation %= 360  # keep rotation in 0-359 degrees

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

    def update(self, dt):
        keys = pygame.key.get_pressed()

        # Rotate left or right
        if keys[pygame.K_a]:
            self.rotate(-1, dt)  # rotate left
        if keys[pygame.K_d]:
            self.rotate(1, dt)   # rotate right

        # Move forward or backward
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)

        # Handle shooting with cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= dt

        if keys[pygame.K_SPACE] and self.shoot_cooldown <= 0:
            self.shoot()
            self.shoot_cooldown = PLAYER_SHOOT_COOLDOWN

    def shoot(self):
        shot = Shot(self.position.x, self.position.y)
        direction = pygame.Vector2(0, 1).rotate(self.rotation)
        shot.velocity = direction * PLAYER_SHOOT_SPEED
