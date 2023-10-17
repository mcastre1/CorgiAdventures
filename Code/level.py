import pygame
from support import import_csv_layout, import_cut_tileset
from settings import tile_size

class Level():
    def __init__(self, display_surface, level_data):
        self.display_surface = display_surface
        self.level_data = level_data

        # Terrain tiles
        terrain_layout = import_csv_layout(self.level_data['terrain'])
        self.terrain_sprites = self.create_sprite_group(terrain_layout, 'terrain')


        self.run()

    def create_sprite_group(self, layout, type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, id in enumerate(row):
                if not id == '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == 'terrain':
                        terrain_tiles_list = import_cut_tileset('./Graphics/terrain/grass/terrain_grass_tiles.png')
                        print('terrain')




    def run(self):
        self.display_surface.fill('black')