import pygame
from support import import_csv_layout, import_cut_tileset
from settings import tile_size
from tiles import StaticTile
from player import Player

class Level():
    def __init__(self, display_surface, level_data):
        self.display_surface = display_surface
        self.level_data = level_data
        self.world_shift = 0

        # Terrain tiles
        # Passing a path to import_csv_layout function
        terrain_layout = import_csv_layout(self.level_data['terrain'])
        # Create a pygame sprite group by passing in the csv list and the type
        self.terrain_sprites = self.create_sprite_group(terrain_layout, 'terrain')

        # Grass
        grass_layout = import_csv_layout(self.level_data['grass'])
        self.grass_sprites = self.create_sprite_group(grass_layout, 'grass')

        # Player setup
        player_layout = import_csv_layout(self.level_data['player'])
        self.player_sprite = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)

        self.run()

    def player_setup(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, id in enumerate(row):
                y = row_index * tile_size   # These two y and x are coordinates for the topleft on a sprite
                x = col_index * tile_size

                if id == '0':
                    self.player_sprite.add(Player((x, y), self.display_surface))


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
    
    # This is where we check for vertical collisions and apply gravity to character
    def vertical_movement_collisions(self):
        player = self.player_sprite.sprite
        player.apply_gravity()
        
        # These are those tiles/sprites that will be unpasable/collidable
        # Add more by concatinating more sprites at the end
        collidable_sprites = self.terrain_sprites.sprites()

        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.on_ceiling = True

                player.direction.y = 0
        
        # This is so player doesnt get stuck on the ground or ceiling.
        if player.on_ground and (player.direction.y < 0 or player.direction.y > 0):
            player.on_ground = False
        if player.on_ceiling and player.direction > 0:
            player.on_ceiling = False

    def horizontal_movement_collision(self):
        player = self.player_sprite.sprite
        player.rect.x += player.direction.x + self.world_shift
        collidable_sprites = self.terrain_sprites.sprites()

        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left


    def run(self):
        self.display_surface.fill('black')

        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)

        self.grass_sprites.update(self.world_shift)
        self.grass_sprites.draw(self.display_surface)

        # player
        self.player_sprite.update(self.world_shift)
        self.vertical_movement_collisions()
        self.horizontal_movement_collision()

        self.player_sprite.draw(self.display_surface)


