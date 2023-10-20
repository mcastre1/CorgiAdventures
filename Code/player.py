import pygame
class Player(pygame.sprite.Sprite):
    def __init__(self, pos, display_surface):
        super().__init__()
        self.image = pygame.image.load('./Graphics/player/idle/idle_0.png')
        self.rect = self.image.get_rect(topleft = (pos))

        self.speed = 5
        self.direction = pygame.math.Vector2(0,0) # This will take care of x and y velocity
        self.jump_speed = -16
        self.gravity = 0.8

        # status
        self.status = 'idle'
        self.facing_right = False


    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.direction.x = -self.speed
            self.facing_right = False
        elif keys[pygame.K_RIGHT]:
            self.direction.x = self.speed
            self.facing_right = True
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE]:
            self.jump()
            print("jump")

    def jump(self):
        self.direction.y = self.jump_speed

    def update_pos(self, shift):
        self.rect.x += shift + self.direction.x
        self.rect.y += self.direction.y

    def apply_gravity(self):
        self.direction.y += self.gravity

    def update(self, shift):
        self.input()
        self.apply_gravity()
        self.update_pos(shift)

