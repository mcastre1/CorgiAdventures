import pygame
from support import import_csv_layout, import_cut_tileset
from settings import tile_size
from tiles import StaticTile

class Level():
    def __init__(self, display_surface, level_data):
        self.display_surface = display_surface
        self.level_data = level_data
        self.world_shift = -1

        # Terrain tiles
        # Passing a path to import_csv_layout function
        terrain_layout = import_csv_layout(self.level_data['terrain'])
        # Create a pygame sprite group by passing in the csv list and the type
        self.terrain_sprites = self.create_sprite_group(terrain_layout, 'terrain')

        # Grass
        grass_layout = import_csv_layout(self.level_data['grass'])
        self.grass_sprites = self.create_sprite_group(grass_layout, 'grass')

        # Player
        player_layout = import_csv_layout(self.level_data['player'])
        self.player_sprite = self.create_sprite_group(player_layout, 'player')
        #self.player_sprite = pygame.sprite.GroupSingle()


        self.run()

    def create_sprite_group(self, layout, type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, id in enumerate(row):
                if not id == '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == 'terrain':
                        terrain_tiles_list = import_cut_tileset('./Graphics/terrain/grass/32terrain_grass_tiles.png')
                        tile_surface = terrain_tiles_list[int(id)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)

                    if type == 'grass':
                        grass_tile_list = import_cut_tileset('./Graphics/decoration/grass/grass_deco_tiles.png')
                        tile_surface = grass_tile_list[int(id)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)

                    sprite_group.add(sprite)

        return sprite_group




    def run(self):
        print(self.player_sprite)
        self.display_surface.fill('black')

        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)

        self.grass_sprites.update(self.world_shift)
        self.grass_sprites.draw(self.display_surface)

        self.player_sprite.draw(self.display_surface)