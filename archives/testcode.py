#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 22 08:33:53 2021

@author: marc
"""


import pygame
pygame.init()

class Button():
    
    def __init__(self):
        self.sprite_sheet = pygame.image.load('Assets/Buttons/Menu Buttons sprite (BnW)_ecrasee.png')
        self.image = self.get_image(0,0)
        self.image = pygame.transform.scale(self.image, (60,20))
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        
        
    def get_image(self, x, y):
        image = pygame.Surface([600,200])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 600,200))
        return image

screen = pygame.display.set_mode((1080,720))

running = True

while running:
    screen.fill((255,255,255))
    button = Button()
    screen.blit(button.image,(200,200))
    pygame.display.flip()
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            running = False
    pygame.display.update()
pygame.quit()