import sys
import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
dt = 0

# Create groups
updatables = pygame.sprite.Group()
drawables = pygame.sprite.Group()
asteroids = pygame.sprite.Group()
shots = pygame.sprite.Group()


# Register containers for sprite classes
Player.containers = (updatables, drawables)
Asteroid.containers = (asteroids, updatables, drawables)
AsteroidField.containers = (updatables,)
Shot.containers = (shots, updatables, drawables)

# Create game objects (auto-added to groups)
player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
asteroid_field = AsteroidField()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    updatables.update(dt)

    # Player-asteroid collision
    for asteroid in asteroids:
        if asteroid.collides_with(player):
            print("Game over!")
            pygame.quit()
            sys.exit()

    # Shot-asteroid collision (asteroids split, shots removed)
    for asteroid in list(asteroids):  # Use list to avoid modifying group during iteration
        for shot in list(shots):
            if asteroid.collides_with(shot):
                asteroid.split()  # split() handles kill() and spawning smaller asteroids
                shot.kill()
                break  # No need to check other shots once asteroid is split

    screen.fill("black")

    for obj in drawables:
        obj.draw(screen)

    pygame.display.flip()
    dt = clock.tick(60) / 1000