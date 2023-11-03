import csv
import pygame
from settings import tile_size

def import_csv_layout(path):
    layout = []

    with open(path) as file:
        csvFile = csv.reader(file)

        for line in csvFile:
            layout.append(line)

    return layout

# Cuts up a tileset and returns a list of all tiles int it of size tile_size
def import_cut_tileset(path):
    surface = pygame.image.load(path).convert_alpha()
    tile_num_x = int(surface.get_width()/tile_size)
    tile_num_y = int(surface.get_height()/tile_size)

    cut_tiles = []

    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * tile_size
            y = row * tile_size

            # Cut out the sprite of size tile_size * 2, at x and y coordinates
            new_surf = pygame.Surface((tile_size, tile_size), flags=pygame.SRCALPHA)
            new_surf.blit(surface, (0,0), pygame.Rect(x, y, tile_size, tile_size))
            cut_tiles.append(new_surf)

    return cut_tiles

# Used whenever we have a sprite with different size than tile_size
def import_cut_tileset_size(path, size):
    surface = pygame.image.load(path).convert_alpha()
    tile_num_x = int(surface.get_width()/size)
    tile_num_y = int(surface.get_height()/size)

    cut_tiles = []

    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * size
            y = row * size

            # Cut out the sprite of size tile_size * 2, at x and y coordinates
            new_surf = pygame.Surface((size, size), flags=pygame.SRCALPHA)
            new_surf.blit(surface, (0,0), pygame.Rect(x, y, size, size))
            cut_tiles.append(new_surf)

    return cut_tiles