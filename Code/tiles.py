import pygame
from support import import_cut_tileset_size
import random
class Tile(pygame.sprite.Sprite):
    def __init__(self, size, x, y):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft=(x,y))

    def update(self, shift):
        self.rect.x += shift

class StaticTile(Tile):
    def __init__(self, size, x, y, surface):
        super().__init__(size, x, y)
        self.image = surface

class Cloud(StaticTile):
    def __init__(self, size, x, y, surface):
        super().__init__(size, x, y, surface)
        self.iamge = surface
        self.last_move = pygame.time.get_ticks()
        self.direction = random.choice([1,-1])

    def update(self, shift):
        if pygame.time.get_ticks() - self.last_move > 1000:
            self.rect.x += self.direction * 1
            self.last_move = pygame.time.get_ticks()

        self.rect.x += shift



class Dust(StaticTile):
    def __init__(self, size, x, y, surface, path, over_size):
        super().__init__(size, x, y, surface)
        self.path = path
        self.tiles = import_cut_tileset_size(path, over_size)
        print(len(self.tiles))
        self.frame_index = 0

    def animate(self):
        self.frame_index += .15
        if int(self.frame_index) >= len(self.tiles):
            self.kill()
        else:
            self.image = self.tiles[int(self.frame_index)]
        print(int(self.frame_index))

    def update(self, shift):
        self.animate()
        self.rect.x += shift



