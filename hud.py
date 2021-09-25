import pygame
import os
import sys
import numpy as np
from settings import DISPLAY

class HUD (pygame.sprite.Sprite):
    
    def __init__(self, level_map, player_health, max_health):
        super().__init__()
        self.minimap = Minimap(level_map)
        self.health_bar = Health_Bar(player_health, max_health)
    
    def draw(self, surface, current_room, rooms):
        self.minimap.draw(surface, current_room, rooms)
        self.health_bar.draw(surface)
    
    def update(self, current_room, player_health):
        self.minimap.update(current_room)    
        self.health_bar.update(player_health)
       
        
        
class Minimap(pygame.sprite.Sprite):
    
    def __init__(self, level_map):
        self.level_map = level_map
        self.minimap_zoom = False
                
    def cleared_rooms(self, current_room):
        current_room.is_cleared = True
        
    def get_inputs(self):
        pressed_key = pygame.key.get_pressed()
        if pressed_key[pygame.K_TAB]:
            self.minimap_zoom = True
        else:
            self.minimap_zoom = False
                    
    def draw(self, surface, current_room, rooms):
        if self.minimap_zoom == False:
            minimap = pygame.Surface((17, 17))
            for room in rooms:
                for x in range(current_room.pos[0] - 1, current_room.pos[0] + 2, 1):
                    for y in range(current_room.pos[1] - 1, current_room.pos[1] + 2, 1):
                        if x < 0 :
                            x = 0
                        elif x > self.level_map.shape[0] - 1:
                            x = self.level_map.shape[0] - 1
                        if y < 0 :
                            y = 0
                        elif y > self.level_map.shape[1] - 1:
                            y = self.level_map.shape[1] - 1
                        rect = pygame.Rect((y - current_room.pos[1] + 1)*5 + 1, (x - current_room.pos[0] + 1)*5 + 1, 5, 5)
                        if room.pos[0] == x and room.pos[1] == y:
                            if room.is_cleared:
                                if room.north:
                                    n = "n_"
                                else:
                                    n = ""
                                if room.south:
                                    s = "s_"
                                else:
                                    s = ""
                                if room.east:
                                    e = "e_"
                                else:
                                    e = ""
                                if room.west:
                                    w = "w_"
                                else:
                                    w = ""
                                image = pygame.image.load(os.getcwd()+"/Assets/Sprites/Own/Perso/minimap/"+ n + w + s + e +"room.png").convert_alpha()
                                if x == current_room.pos[0] and y == current_room.pos[1]:
                                    image.fill((255,0,0,50), special_flags = pygame.BLEND_RGBA_ADD)
                                minimap.blit(image,rect)
            surface.blit(pygame.transform.scale(minimap, (50,50)), (DISPLAY[0] - 70, 20))
        else:
            minimap = pygame.Surface((5*self.level_map.shape[0] + 2, 5*self.level_map.shape[1] + 2))
            for room in rooms:
                for x in range(self.level_map.shape[0]):
                    for y in range(self.level_map.shape[1]):
                        if x < 0 :
                            x = 0
                        elif x > self.level_map.shape[0] - 1:
                            x = self.level_map.shape[0] - 1
                        if y < 0 :
                            y = 0
                        elif y > self.level_map.shape[1] - 1:
                            y = self.level_map.shape[1] - 1
                        rect = pygame.Rect(y*5 + 1, x*5 + 1, 5, 5)
                        if room.pos[0] == x and room.pos[1] == y:
                            if room.is_cleared:
                                if room.north:
                                    n = "n_"
                                else:
                                    n = ""
                                if room.south:
                                    s = "s_"
                                else:
                                    s = ""
                                if room.east:
                                    e = "e_"
                                else:
                                    e = ""
                                if room.west:
                                    w = "w_"
                                else:
                                    w = ""
                                image = pygame.image.load(os.getcwd()+"/Assets/Sprites/Own/Perso/minimap/"+ n + w + s + e +"room.png").convert_alpha()                                
                                if x == current_room.pos[0] and y == current_room.pos[1]:
                                    image.fill((255,0,0,50), special_flags = pygame.BLEND_RGBA_ADD)
                                minimap.blit(image,rect)
            minimap.set_alpha(200)
            surface.blit(pygame.transform.scale(minimap, (200,200)), (2*DISPLAY[0]/3, 20))
        
    def update(self, current_room):
        self.get_inputs()
        self.cleared_rooms(current_room)
        
        

class Health_Bar(pygame.sprite.Sprite):
    
    def __init__(self, health, max_health):
        self.health = health
        self.full_heart, self.half_heart, self.empty_heart = self.get_images()
        self.full_heart_rect = self.full_heart.get_rect()
        self.half_heart_rect = self.half_heart.get_rect()
        self.empty_heart_rect = self.empty_heart.get_rect()
        self.max_health = max_health

    def get_images(self):
        full_heart = pygame.image.load(os.getcwd()+"/Assets/Sprites/Own/Perso/full_heart.png").convert()
        half_heart = pygame.image.load(os.getcwd()+"/Assets/Sprites/Own/Perso/half_heart.png").convert()
        empty_heart = pygame.image.load(os.getcwd()+"/Assets/Sprites/Own/Perso/empty_heart.png").convert()
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
            surface.blit(pygame.transform.scale2x(self.full_heart),(self.full_heart_rect[0] + 5 + 2*14*full_heart, self.full_heart_rect[1] + 5, self.full_heart_rect[2], self.full_heart_rect[3]))
        if self.nb_half_heart == 1:
            surface.blit(pygame.transform.scale2x(self.half_heart),(self.half_heart_rect[0] + 5 + 2*14*(self.nb_full_heart), self.half_heart_rect[1] + 5, self.half_heart_rect[2], self.half_heart_rect[3]))
        for empty_heart in range(self.nb_empty_heart):
            surface.blit(pygame.transform.scale2x(self.empty_heart),(self.empty_heart_rect[0] + 5 + 2*14*(self.nb_full_heart + self.nb_half_heart + empty_heart), self.empty_heart_rect[1] + 5, self.empty_heart_rect[2], self.empty_heart_rect[3]))

    def update(self,player_health):
        self.get_hearts(player_health)
        