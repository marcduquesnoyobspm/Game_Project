import pygame
import os
from settings import tile_size

class Tile(pygame.sprite.Sprite):

    def __init__(self, name, orientation, x, y):
        super().__init__()
        self.name = name
        self.orientation = orientation
        self.pos = [x * tile_size, y * tile_size]
        self.image, self.rect = self.get_image()
    
    def get_image(self):
        image = pygame.image.load(os.getcwd()+"/Assets/Sprites/Own/Perso/" + self.name + ".png").convert_alpha()
        if self.orientation == "N":
            rect = image.get_rect(topleft = self.pos)
        elif self.orientation == "S":
            rect = image.get_rect(topleft = self.pos)
            image = pygame.transform.rotate(image, 180)
        elif self.orientation == "W":
            rect = image.get_rect(topleft = self.pos)
            image = pygame.transform.rotate(image, 90)
        elif self.orientation == "E":
            rect = image.get_rect(topleft = self.pos)
            image = pygame.transform.rotate(image, -90)
        return image, rect

    def draw(self, surface):
        surface.draw(self.image, self.rect)
        
class Door(pygame.sprite.Sprite):

    def __init__(self, name, orientation, x, y):
        super().__init__()
        self.name = name
        self.orientation = orientation
        self.pos = (x,y)
        self.image, self.rect = self.get_image()
        
    def get_image(self):
        image = pygame.image.load(os.getcwd()+"/Assets/Sprites/Own/Perso/" + self.name + ".png").convert_alpha()
        if self.orientation == "N":
            rect = image.get_rect(midtop = self.pos)
        elif self.orientation == "S":
            rect = image.get_rect(midbottom = self.pos)
            image = pygame.transform.rotate(image, 180)
        elif self.orientation == "W":
            rect = image.get_rect(midleft = self.pos)
            image = pygame.transform.rotate(image, 90)
        elif self.orientation == "E":
            rect = image.get_rect(midright = self.pos)
            image = pygame.transform.rotate(image, -90)
        return image, rect

    def draw(self, surface):
        surface.draw(self.image, self.rect)