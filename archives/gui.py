import pygame
import numpy as np

pygame.init()

class GUI():

    def __init__(self):
        self.full_heart, self.half_heart, self.empty_heart = self.get_images()
        self.full_heart_rect = self.full_heart.get_rect()
        self.half_heart_rect = self.half_heart.get_rect()
        self.empty_heart_rect = self.empty_heart.get_rect()
        self.max_health = 3

    def get_images(self):
        full_heart = pygame.image.load("Assets\Sprites\Own\Perso/full_heart.png").convert()
        half_heart = pygame.image.load("Assets\Sprites\Own\Perso/half_heart.png").convert()
        empty_heart = pygame.image.load("Assets\Sprites\Own\Perso/empty_heart.png").convert()
        full_heart.set_colorkey((255,255,255))
        half_heart.set_colorkey((255,255,255))
        empty_heart.set_colorkey((255,255,255))
        return full_heart, half_heart, empty_heart

    def get_hearts(self,player_health):
        self.nb_full_heart = int(player_health)
        self.nb_empty_heart = int(self.max_health - np.ceil(player_health))
        if self.nb_empty_heart + self.nb_full_heart != self.max_health:
            self.nb_half_heart = 1
        else:
            self.nb_half_heart = 0
    
    def draw(self,surface):
        for full_heart in range(self.nb_full_heart):
            surface.blit(self.full_heart,(self.full_heart_rect[0] + 5 + 14*full_heart, self.full_heart_rect[1] + 5, self.full_heart_rect[2], self.full_heart_rect[3]))
        if self.nb_half_heart == 1:
            surface.blit(self.half_heart,(self.half_heart_rect[0] + 5 + 14*(self.nb_full_heart), self.half_heart_rect[1] + 5, self.half_heart_rect[2], self.half_heart_rect[3]))
        for empty_heart in range(self.nb_empty_heart):
            surface.blit(self.empty_heart,(self.empty_heart_rect[0] + 5 + 14*(self.nb_full_heart + self.nb_half_heart + empty_heart), self.empty_heart_rect[1] + 5, self.empty_heart_rect[2], self.empty_heart_rect[3]))

    def other_draw(self,surface,player_health):
        percent_max_health_rect = pygame.Rect(5,5,100,5)
        percent_player_health = player_health*100/self.max_health
        percent_player_health_rect = pygame.Rect(5,5,int(percent_player_health),5)
        pygame.draw.rect(surface, (255,0,0), percent_player_health_rect, width = 0, border_radius = 10)
        pygame.draw.rect(surface, (0,0,0), percent_max_health_rect, width = 2, border_radius = 10)

    def update(self,player_health):
        self.get_hearts(player_health)