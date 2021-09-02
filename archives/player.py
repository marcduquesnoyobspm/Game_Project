#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 24 19:41:32 2021

@author: marc
"""


import pygame
import numpy as np
import glob
import os


pygame.init()

class Player(pygame.sprite.Sprite):
    
    def __init__(self, position, health, attack):
        super().__init__()
        self.is_jumping = False
        self.is_slashing = False
        self.is_blastering = False
        self.is_running = False
        self.is_falling = False
        self.new_anim = False
        self.mirror = False
        self.action = "Idle"
        self.actions_names = ["Dash", "Death", "GetHit", "Idle", "Jump", "Run", "Slash_no_effect", "Slash_only_effect", "Slash", "Blaster"] 
        self.sprites = self.get_sprites()
        del self.sprites["Jump"][0]
        self.group = self.sprites[self.action]
        self.health = health
        self.attack = attack
        self.speed = 5
        self.jump_speed = -200
        self.gravity = 400
        self.jump_time = 0
        self.tick = 0
        self.image = self.group[0]
        self.rect = self.image.get_rect()
        self.size = self.image.get_size()
        self.x, self.y = position[0], position[1]
        self.current_sprite = 0
        self.jump_sprite = 0
        self.cooldown_idle = 300
        self.offset = 0
        self.y_origin = self.y
        
    def get_sprites(self):
        dir = os.path.abspath(os.getcwd())
        sprites_paths = np.sort(glob.glob(dir + "/Assets/Sprites/Striker/*"))

        sprites = {}
        sprites_set = [pygame.image.load(path).convert_alpha() for path in sprites_paths]
        for name, i in zip(self.actions_names, range(len(sprites_set))):
            sprites[name] = []
            for j in range(16):
                if i == 6 or i == 7:
                    sprites[name].append(pygame.transform.scale2x(sprites_set[i].subsurface([j*128,0,128,96])))
                if i == 1:
                    sprites[name].append(pygame.transform.scale2x(sprites_set[i].subsurface([j*96,0,96,96])))
            for j in range(4):
                if i == 2:
                    sprites[name].append(pygame.transform.scale2x(sprites_set[i].subsurface([j*96,0,96,96])))
            for j in range(12):
                if i == 0:
                    sprites[name].append(pygame.transform.scale2x(sprites_set[i].subsurface([j*96,0,96,96])))
            for j in range(8): 
                if i == 8:
                    sprites[name].append(pygame.transform.scale2x(sprites_set[i].subsurface([j*128,0,128,96])))
                if i == 3 or i == 5 or i == 4:
                    sprites[name].append(pygame.transform.scale2x(sprites_set[i].subsurface([j*96,0,96,96])))
            for j in range(6):
                if i == 9:
                    sprites[name].append(pygame.transform.scale2x(sprites_set[i].subsurface([(10+j)*128,0,128,96])))
        return sprites

    def get_damaged(self, hit):
        self.health = self.health - hit
        
    def get_healed(self, heal):
        self.health = self.health + heal
            
    def move(self, deplacement):
        self.x, self.y = self.x + deplacement[0]*self.speed, self.y + deplacement[1]*self.speed
        
    def jump(self):
        if self.is_jumping:
            self.jump_time += self.tick/1000
            self.y = self.gravity*(self.jump_time**2)/2 + self.jump_speed*self.jump_time + self.y_origin
            if self.y >= self.y_origin:
                self.is_jumping = False
                self.jump_time = 0
    
    def animation(self):
        if self.is_blastering:
            length = len(self.sprites["Blaster"])
        if self.is_slashing:
            length = len(self.sprites["Slash"])
        if self.is_blastering == False and self.is_slashing == False:
            if self.is_running:
                length = len(self.sprites["Run"])
            else:
                length = len(self.sprites["Idle"])
        if self.action == "Jump":
            self.image = self.group[np.int(self.jump_sprite)]
        else:
            if self.current_sprite < length:
                self.image = self.group[np.int(self.current_sprite)]
        self.jump_sprite += 0.15
        self.current_sprite += 0.15

        if self.mirror:
            self.image = pygame.transform.flip(self.image, True, False)
        else:
            pass
        self.rect = self.image.get_rect()
        self.size = self.image.get_size()
        
        if self.is_blastering or self.is_slashing:
            self.offset = 128 - 96
        else:
            self.offset = 0
        if self.mirror:
            self.rect.center = (self.x - self.offset, self.y)
        else:
            self.rect.center = (self.x + self.offset, self.y)
            
        if self.current_sprite >= length:
            self.current_sprite = 0
            self.new_anim = False
            self.is_running = False
            self.is_blastering = False
            self.is_slashing = False

        if self.jump_sprite >= len(self.sprites["Jump"]):
            self.jump_sprite = 0
            
        
        
        self.jump()
            
    def def_group(self):
        if self.new_anim:
            self.current_sprite = 0
            self.new_anim = False
        if self.is_slashing:
            self.action = "Slash"
        if self.is_blastering:
            self.action = "Blaster"
        if self.is_slashing or self.is_blastering:
            pass
        else:
            if self.is_jumping:
                self.action = "Jump"
            else:
                if self.is_running:
                    self.action = "Run"
                else: 
                    self.action = "Idle"
                    
        

                
    def update(self):
        self.def_group()
        self.group = self.sprites[self.action]
        self.animation()
        
        
        