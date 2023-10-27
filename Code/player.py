import pygame
from support import import_cut_tileset

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, display_surface):
        super().__init__()
        self.display_surface = display_surface
        self.image = pygame.image.load('./Graphics/player/idle/idle_0.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = (pos))

        self.speed = .5
        self.direction = pygame.math.Vector2(0,0) # This will take care of x and y velocity
        self.jump_speed = -12
        self.gravity = 0.8

        # status
        self.status = 'idle'
        self.facing_right = False
        self.on_ground = True
        self.on_ceiling = False

        # atts
        self.max_health = 10
        self.current_health = 10

        #animations
        self.animations = {'idle':[],
                           'walk':[]}
        self.sprite_index = 0
        self.sprite_speed = 0.1
        
        # get animations
        for key in self.animations.keys():
            self.animations[key] = import_cut_tileset(f'./Graphics/player/{key}/{key}.png')
            print(key)


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

        if keys[pygame.K_SPACE] and self.on_ground:
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
        self.current_health -= 1

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def get_status(self):
        if int(self.direction.y) < 0:
            #self.status = 'jump'
            print('jumping')
        # This elif had to be converted into an int because the double 0.0 was making
        # this branch true.
        elif int(self.direction.y) > 0:
            #self.status = 'fall'
            print('falling')
        else:
            # This else branch checks whether we are walking right, left, or idle
            if int(self.direction.x) > 0:
                self.status = 'walk'
                self.sprite_speed = 0.2
            elif int(self.direction.x) < 0:
                self.status = 'walk'
                self.sprite_speed = 0.2
            elif int(self.direction.x) == 0:
                self.status = 'idle'
                self.sprite_speed = 0.1

    def display_health(self):
        max_rect = pygame.Rect(1, 2, 150, 20)
        percentage_health = self.current_health/self.max_health
        current_rect = pygame.Rect(3, 4, (max_rect.width*percentage_health )- 4, 16)
        pygame.draw.rect(self.display_surface, 'black', max_rect, 2)
        pygame.draw.rect(self.display_surface, 'red', current_rect)


    def update(self, shift):
        self.input()
        self.get_status()
        self.animate()
        self.display_health()

