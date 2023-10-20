import pygame
from settings import *
import sys
from level import Level
from game_data import level_0

# Pygame initialization
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('CorigAdventures')
clock = pygame.time.Clock()

level = Level(screen, level_0)

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    level.run()

    pygame.display.update()
    clock.tick(60)

s