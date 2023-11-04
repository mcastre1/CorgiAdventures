import pygame
from support import import_csv_layout, import_cut_tileset
from settings import tile_size, screen_width, screen_height
from tiles import StaticTile, Cloud
from particles import Dust
from player import Player
from game_data import level_0
from random import choice, randint

class Level():
    def __init__(self, display_surface, level_data):
        self.display_surface = display_surface
        self.level_data = level_data
        self.world_shift = 0

        # Background sprites
        background_layout = import_csv_layout(self.level_data['background'])
        self.background_sprites = self.create_sprite_group(background_layout, 'background')

        # Terrain tiles
        # Passing a path to import_csv_layout function
        terrain_layout = import_csv_layout(self.level_data['terrain'])
        # Create a pygame sprite group by passing in the csv list and the type
        self.terrain_sprites = self.create_sprite_group(terrain_layout, 'terrain')

        # Grass
        grass_layout = import_csv_layout(self.level_data['grass'])
        self.grass_sprites = self.create_sprite_group(grass_layout, 'grass')

        # Bushes
        bushes_layout = import_csv_layout(self.level_data['bush'])
        self.bush_sprites = self.create_sprite_group(bushes_layout, 'bush')

        # Player setup
        player_layout = import_csv_layout(self.level_data['player'])
        self.player_sprite = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)

        # Particles
        self.particles = pygame.sprite.Group()

        # Clouds
        self.level_width_pixels = len(terrain_layout[0]) * tile_size
        self.number_clouds = 10
        self.cloud_sprites = [pygame.image.load('./Graphics/decoration/clouds/small.png'),
                              pygame.image.load('./Graphics/decoration/clouds/big.png')]
        self.cloud_group = self.generate_clouds()

        self.run()

    def add_particle(self, pos):
        self.particles.add(Dust(4, pos[0], pos[1], surface=None, path="./Graphics/player/dust_particles/running.png", over_size=4))


    def generate_clouds(self):
        group = pygame.sprite.Group()
        max_x = self.level_width_pixels
        max_y = int(screen_height/2.5)

        for _ in range(self.number_clouds):
            group.add(Cloud(tile_size, randint(0, max_x), randint(0, max_y), choice(self.cloud_sprites)))

        return group


    def player_setup(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, id in enumerate(row):
                y = row_index * tile_size   # These two y and x are coordinates for the topleft on a sprite
                x = col_index * tile_size

                if id == '0':
                    self.player_sprite.add(Player((x, y), self.display_surface, self.add_particle))


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

                    if type == 'bush':
                        bush_tile = import_cut_tileset('./Graphics/decoration/bushes/small_bush.png')
                        tile_surface = bush_tile[int(id)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)

                    if type == 'background':
                        background_image = pygame.image.load("./Graphics/background/id_1.png")
                        sprite = StaticTile(tile_size, x, y - screen_height, background_image)

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
            if player.rect.colliderect(sprite.rect):
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
        if player.on_ceiling and player.direction.y > 0:
            player.on_ceiling = False

    # Takes care of horizontal movement and collisions on the x axis
    def horizontal_movement_collision(self):
        # Movement
        player = self.player_sprite.sprite
        player.rect.x += player.direction.x * player.speed
        
        if player.is_dashing:
            player.rect.x += player.direction.x * 5

        # collisions
        collidable_sprites = self.terrain_sprites.sprites()
        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left

    def scroll_x(self):
        player = self.player_sprite.sprite
        player_x = player.rect.centerx

        # Temp world shift variable for dashing,
        # If dashing we incerement the speed at which the scroll x happens
        # to keep up with character movement.
        temp_world_shift = 5
        if player.is_dashing:
            temp_world_shift = 30

        if player_x < (screen_width * .33) and player.direction.x < 0:
            self.world_shift = temp_world_shift
            player.speed = 0
        elif player_x > (screen_width * .66) and player.direction.x > 0:
            self.world_shift = -1 * temp_world_shift
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 5


    def run(self):
        self.display_surface.fill('blue')

        # background
        self.background_sprites.update(self.world_shift)
        self.background_sprites.draw(self.display_surface)
        
        # clouds
        self.cloud_group.update(self.world_shift)
        self.cloud_group.draw(self.display_surface)
        
        # Terrain
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)

        # Bushes decoration
        self.bush_sprites.update(self.world_shift)
        self.bush_sprites.draw(self.display_surface)

        # Grass decoration
        self.grass_sprites.update(self.world_shift)
        self.grass_sprites.draw(self.display_surface)

        # player
        self.player_sprite.update(self.world_shift)
        self.horizontal_movement_collision()
        self.vertical_movement_collisions()

        self.player_sprite.draw(self.display_surface)
        
        self.particles.update(self.world_shift)
        self.particles.draw(self.display_surface)
        self.scroll_x()        

        


