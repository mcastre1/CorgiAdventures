import pygame

class Level():
    def __init__(self, display_surface):
        self.display_surface = display_surface
        self.run()

    def run(self):
        self.display_surface.fill('black')