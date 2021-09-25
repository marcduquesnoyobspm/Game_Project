#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 26 18:29:54 2021

@author: marc
"""


import pygame
import os

pygame.init()

class Bullet(pygame.sprite.Sprite):
    
    def __init__(self, x, y, direction, damage):
        super().__init__()
        self.pos = [x,y]
        self.shoot = direction
        self.damage = damage
        self.speed = 10
        self.image = self.get_image()
        self.rect = self.image.get_rect(center = self.pos)
        
        
    def get_image(self):
        image = pygame.image.load(os.getcwd()+"/Assets/Sprites/Own/Perso/bullet.png").convert_alpha()
        if self.shoot.x == -1:
            image = pygame.transform.rotate(image, 180)
        elif self.shoot.y == 1:
            image = pygame.transform.rotate(image, -90)
        elif self.shoot.y == -1:
            image = pygame.transform.rotate(image, 90)
        return image
        
    def draw(self, surface):
        surface.blit(self.image, self.rect)
    
    def update(self):
        self.rect.center = self.rect.centerx + self.speed*self.shoot.x, self.rect.centery + self.speed*self.shoot.y