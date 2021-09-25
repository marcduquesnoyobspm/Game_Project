#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 24 11:43:36 2021

@author: marc
"""


import pygame
import os


class Enemy(pygame.sprite.Sprite):
    
    def __init__(self, name, x, y, health, attack, speed):
        super().__init__()
        self.pos = [x,y]
        self.name = name
        self.health = health
        self.attack = attack
        self.speed = speed
        self.direction = pygame.math.Vector2(0,0)
        self.start_moving = 0
        self.is_dead = False
        self.image = self.get_image()
        self.rect = self.image.get_rect(midbottom = (x,y))
        
    def get_image(self):
        image = pygame.image.load(os.getcwd()+"/Assets/Sprites/Own/Perso/"+ self.name +".png").convert_alpha()
        image.set_colorkey((255,255,255))
        return image
    
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
                    
    def death(self):
        if self.health <= 0:
            self.is_dead = True
        
    def draw(self, surface):
        surface.blit(self.image, self.rect)
    
    def update(self, collide_function):
        self.move(collide_function)
        self.pos = self.rect.midbottom
        self.death()