import pygame
class Player(pygame.sprite.Sprite):
    def __init__(self, pos, display_surface):
        super().__init__()
        self.image = pygame.image.load('./Graphics/player/idle/idle_0.png')
        self.rect = self.image.get_rect(topleft = (pos))

        self.speed = 5
        self.y_velocity = 0
        self.x_velocity = 0

        # status
        self.status = 'idle'
        self.facing_right = False


    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x_velocity = -self.speed
            self.facing_right = False
        elif keys[pygame.K_RIGHT]:
            self.x_velocity = self.speed
            self.facing_right = True
        else:
            self.x_velocity = 0

        if keys[pygame.K_SPACE]:
            self.jump()

    def jump(self):
        pass

    def update_pos(self, shift):
        self.rect.x += shift + self.x_velocity

    def update(self, shift):
        self.input()
        self.update_pos(shift)

