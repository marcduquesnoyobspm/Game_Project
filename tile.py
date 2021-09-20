import pygame
from settings import tile_size

class Tile(pygame.sprite.Sprite):

    def __init__(self, name, x, y):
        super().__init__()
        self.name = name
        self.image = self.get_image()
        self.size = self.image.get_size()
        self.rect = pygame.Rect(x * tile_size, y * tile_size, self.size[0], self.size[0])
    
    def get_image(self):
        image = pygame.image.load("Assets\Sprites\Own\Perso/" + self.name + ".png").convert_alpha()
        return image

    def draw(self, surface):
        surface.draw(self.image, self.rect)