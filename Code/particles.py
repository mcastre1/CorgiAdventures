from tiles import *

class Dust(StaticTile):
    def __init__(self, size, x, y, surface, path, over_size):
        super().__init__(size, x, y, surface)
        self.path = path
        self.tiles = import_cut_tileset_size(path, over_size)
        self.frame_index = 0

    # Change between active frame picture
    def animate(self):
        self.frame_index += .15
        if int(self.frame_index) >= len(self.tiles):
            self.kill()
        else:
            self.image = self.tiles[int(self.frame_index)]

    def update(self, shift):
        self.animate()
        self.rect.x += shift