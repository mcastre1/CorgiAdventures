import pygame
from support import import_cut_tileset

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, display_surface, add_particle):
        super().__init__()

        self.add_particle = add_particle

        self.display_surface = display_surface
        self.image = pygame.image.load('./Graphics/player/idle/idle_0.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = (pos))

        self.speed = .5
        self.direction = pygame.math.Vector2(0,0) # This will take care of x and y velocity
        self.jump_speed = -12
        self.gravity = 0.8
        self.dash_direction = 6

        # status
        self.status = 'idle'
        self.facing_right = False
        self.on_ground = True
        self.on_ceiling = False
        self.is_dashing = False

        # Cooldowns
        self.dash_cooldown = 1000
        self.last_dash = 0

        self.walking_dust_cd = 100
        self.last_walk_dust = 0

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

        # For jumping
        if keys[pygame.K_SPACE] and self.on_ground:
            self.jump()

        # For dashing
        if keys[pygame.K_LCTRL]:
            current_time = pygame.time.get_ticks()
          
            if current_time - self.last_dash > self.dash_cooldown:
                self.dash()
                self.last_dash = pygame.time.get_ticks()


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

        if self.on_ground and self.status == 'walk':
            current_time = pygame.time.get_ticks()
            if current_time - self.last_walk_dust >= self.walking_dust_cd:
                if self.facing_right:
                    self.add_particle((self.rect.bottomleft[0], self.rect.bottomleft[1]-3))
                else:
                    self.add_particle((self.rect.bottomright[0], self.rect.bottomright[1]-3))

                self.last_walk_dust = pygame.time.get_ticks()


    def dash(self):
        if self.facing_right:
            self.direction.x = self.dash_direction
        else:
            self.direction.x = -self.dash_direction

    def jump(self):
        self.direction.y = self.jump_speed
        self.current_health -= 1

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def get_status(self):
        if int(self.direction.y) < 0:
            #self.status = 'jump'
            print('jump')
        # This elif had to be converted into an int because the double 0.0 was making
        # this branch true.
        elif int(self.direction.y) > 0:
            #self.status = 'fall'
            print('fall')
        else:
            # This else branch checks whether we are walking right, left, or idle
            if int(self.direction.x) == self.dash_direction or self.direction.x == self.dash_direction * -1: # This will keep track of character dashing movement
                self.is_dashing = True
                print("dash")
            elif int(self.direction.x) > 0:
                self.status = 'walk'
                self.sprite_speed = 0.2
                self.is_dashing = False
            elif int(self.direction.x) < 0:
                self.status = 'walk'
                self.sprite_speed = 0.2
                self.is_dashing = False
            elif int(self.direction.x) == 0:
                self.status = 'idle'
                self.sprite_speed = 0.1
                self.is_dashing = False

    # Create 2 rects to display player health bar
    def display_health(self):
        # This represents the health bar placeholder
        max_rect = pygame.Rect(1, 2, 150, 20)
        # How much health we have left in percentage
        percentage_health = self.current_health/self.max_health
        # Create a rectangle by multiplying the placeholder width by the percentage of health remaining
        current_rect = pygame.Rect(3, 4, (max_rect.width*percentage_health )- 4, 16)

        # Draw both rectangles to the passed in display surface
        pygame.draw.rect(self.display_surface, 'black', max_rect, 2, 3)
        pygame.draw.rect(self.display_surface, (198, 47, 39), current_rect, 0, 2)

    def display_cds(self):
        # Dash
        dash_cd = pygame.Rect(1, 22, 100, 10)
        current_percentage = (pygame.time.get_ticks()-self.last_dash)/self.dash_cooldown
        if current_percentage >= 1:
            current_percentage = 1

        current_rect = pygame.Rect(3, 23, (dash_cd.width*current_percentage - 4), 7)

        pygame.draw.rect(self.display_surface, 'black', dash_cd, 2, 2)
        pygame.draw.rect(self.display_surface, 'gray', current_rect, 0, 1)

    def update(self, shift):
        self.input()
        self.get_status()
        self.animate()
        self.display_health()
        self.display_cds()

