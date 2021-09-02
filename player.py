import pygame

pygame.init()

class Player():

    def __init__(self, x, y):
        self.speed = 2
        self.image = self.get_image()
        self.size = self.image.get_size()
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.collide_rect = pygame.Rect(0,0,5,15)
        self.collide_rect.center = self.rect.center
    
    def get_image(self):
        image = pygame.image.load("Assets\Sprites\Own\Perso\char.png").convert()
        image.set_colorkey((0,0,0))
        return image

    def update(self):
        self.rect.center = self.collide_rect.center[0] + 1, self.collide_rect.center[1] - 1/2