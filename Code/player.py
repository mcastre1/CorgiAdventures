import pygame
from support import import_cut_tileset

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, display_surface):
        super().__init__()
        self.image = pygame.image.load('./Graphics/player/idle/idle_0.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = (pos))

        self.speed = 5
        self.direction = pygame.math.Vector2(0,0) # This will take care of x and y velocity
        self.jump_speed = -8
        self.gravity = 0.8

        # status
        self.status = 'idle'
        self.facing_right = False
        self.on_ground = True
        self.on_ceiling = False

        #animations
        self.animations = {'idle':[]}
        self.sprite_index = 0
        self.sprite_speed = 0.1
        
        # get animations
        for key in self.animations.keys():
            self.animations[key] = import_cut_tileset(f'./Graphics/player/{key}/{key}.png')


    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facing_right = False
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facing_right = True
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE]:
            self.jump()

    def animate(self):
        #image = pygame.image.load('./Graphics/player/idle/idle_0.png').convert_alpha()

        self.sprite_index += self.sprite_speed

        if self.sprite_index >= len(self.animations[self.status]):
            self.sprite_index = 0
        image = self.animations[self.status][int(self.sprite_index)]
        
        if self.facing_right:
            self.image = image
        else:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image

    def jump(self):
        self.direction.y = self.jump_speed

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def update(self, shift):
        self.input()
        self.animate()

