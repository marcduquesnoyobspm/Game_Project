import pygame
import numpy as np
import os
from settings import TARGET_FPS, DISPLAY, tile_size

class Player(pygame.sprite.Sprite):

    def __init__(self,x , y, max_health):
        super().__init__()
        self.pos = [x, y]
        self.speed = 5
        self.health = max_health
        self.max_health = max_health
        self.attack = 1
        self.attack_cooldown = 0
        self.is_vulnerable_cooldown = 0
        self.is_dead = False
        self.is_shooting = False
        self.is_vulnerable = True
        self.direction = pygame.math.Vector2(0,0)
        self.shoot = pygame.math.Vector2(0,0)
        self.image = pygame.image.load(os.getcwd()+"/Assets/Sprites/Own/Perso/char_3.png").convert_alpha()
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect(midbottom = self.pos)
    
    def get_inputs(self):
        self.direction = pygame.math.Vector2(0,0)
        self.shoot = pygame.math.Vector2(0,0)
        pressed_key = pygame.key.get_pressed()
        if pressed_key[pygame.K_q]:
            self.direction.x += -1
        if pressed_key[pygame.K_d]:
            self.direction.x += 1
        if pressed_key[pygame.K_z]:
            self.direction.y += -1
        if pressed_key[pygame.K_s]:
            self.direction.y += 1
        if pressed_key[pygame.K_LEFT]:
            self.shoot.x += -1
            self.is_shooting = True
        elif pressed_key[pygame.K_RIGHT]:
            self.shoot.x += 1
            self.is_shooting = True
        elif pressed_key[pygame.K_UP]:
            self.shoot.y += -1
            self.is_shooting = True
        elif pressed_key[pygame.K_DOWN]:
            self.shoot.y += 1
            self.is_shooting = True
        else:
            self.is_shooting = False

    def move(self, collide_function):
            collision_types = {"Top" : False, "Bottom" : False, "Left" : False, "Right" : False}
            if self.direction == [1,1] or self.direction == [-1, 1] or self.direction == [-1, -1] or self.direction == [1, -1]:
                norm = pygame.math.Vector2.length(self.direction)
            else:
                norm = 1
            self.rect.centerx += 1/norm * self.direction.x * self.speed
            hit_list = collide_function(self.rect.midbottom)
            for tile in hit_list:
                if self.direction.x > 0:
                    self.rect.centerx = tile.rect.left - 2
                    self.direction.x = 0
                    collision_types["Right"] = True
                elif self.direction.x < 0:
                    self.rect.centerx = tile.rect.right + 2
                    self.direction.x = 0
                    collision_types["Left"] = True
                    
            self.rect.bottom += 1/norm * self.direction.y * self.speed
            hit_list = collide_function(self.rect.midbottom)
            for tile in hit_list:
                if self.direction.y > 0:
                    self.rect.bottom = tile.rect.top - 1
                    self.direction.y = 0
                    collision_types["Bottom"] = True
                elif self.direction.y < 0:
                    self.rect.bottom = tile.rect.bottom + 2
                    self.direction.y = 0
                    collision_types["Top"] = True
            
    def check_death(self):
        if self.health <= 0:
            self.health = 0
            self.is_dead = True
        
    def update(self, collide_function):
        self.get_inputs()
        self.move(collide_function)
        self.pos = self.rect.midbottom
        self.check_death()
