#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 24 19:41:32 2021

@author: marc
"""


import pygame
import time
import numpy as np
import glob

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
        self.action = 'Idle'
        self.actions_names = ["Dash", "Death", "GetHit", "Idle", "Jump", "Run", "Slash_no_effect", "Slash_only_effect", "Slash", "Blaster"] 
        self.sprites = {}
        self.get_sprites()
        self.sprites["Slash"].append(self.sprites["Slash"][0])
        self.group = self.sprites["Idle"]
        self.health = health
        self.attack = attack
        self.speed = 10
        self.jump_speed = 10
        self.jump_time = 0
        self.image = self.group[0]
        self.rect = self.image.get_rect()
        self.size = self.image.get_size()
        self.x, self.y = position[0], position[1]
        self.current_sprite = 0
        self.jump_sprite = 0
        self.cooldown_idle = 300
        self.offset = 0
        self.y_origin = self.y
        self.last = pygame.time.get_ticks()
        
    def get_sprites(self):
        sprites_paths = np.sort(glob.glob("/home/marc/Projects/Game/Assets/Sprites/Striker/*"))
        sprites_set = [pygame.image.load(path).convert_alpha() for path in sprites_paths]
        for name, i in zip(self.actions_names, range(len(sprites_set))):
            self.sprites[name] = []
            
            for j in range(16):
                if i == 6 or i == 7:
                    self.sprites[name].append(pygame.transform.scale2x(sprites_set[i].subsurface([j*128,0,128,96])))
                if i == 1:
                    self.sprites[name].append(pygame.transform.scale2x(sprites_set[i].subsurface([j*96,0,96,96])))
            for j in range(4):
                if i == 2:
                    self.sprites[name].append(pygame.transform.scale2x(sprites_set[i].subsurface([j*96,0,96,96])))
            for j in range(12):
                if i == 0 or i == 4:
                    self.sprites[name].append(pygame.transform.scale2x(sprites_set[i].subsurface([j*96,0,96,96])))
            for j in range(8): 
                if i == 8:
                    self.sprites[name].append(pygame.transform.scale2x(sprites_set[i].subsurface([j*128,0,128,96])))
                if i == 3 or i == 5:
                    self.sprites[name].append(pygame.transform.scale2x(sprites_set[i].subsurface([j*96,0,96,96])))
            for j in range(6):
                if i == 9:
                    self.sprites[name].append(pygame.transform.scale2x(sprites_set[i].subsurface([(10+j)*128,0,128,96])))
                
    def get_damaged(self, hit):
        self.health = self.health - hit
        
    def get_healed(self, heal):
        self.health = self.health + heal
            
    def move(self, deplacement):
        self.x, self.y = self.x + deplacement[0]*self.speed, self.y + deplacement[1]*self.speed
        
    def jump(self):
        pass
    
    def animation(self):
        self.jump_sprite += 0.1
        self.current_sprite += 0.1
        if self.current_sprite >= len(self.group):
            self.current_sprite = 0
            self.new_anim = False
            if self.is_running or self.is_slashing or self.is_blastering:
                pass
            else:
                self.group = self.sprites["Idle"]
        if self.jump_sprite >= len(self.sprites["Jump"]):
            self.jump_sprite = 0
            if self.is_jumping:
                pass
            else:
                self.group = self.sprites["Idle"]
        if self.action == "Jump":
            self.image = self.group[np.int(self.jump_sprite)]
        else:
            self.image = self.group[np.int(self.current_sprite)]
            
    def def_group(self):
        now = pygame.time.get_ticks()
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
            elif self.is_running:
                self.action = "Run"
            else:
                if now - self.last > 0.2:
                    self.action = "Idle"
        self.group = self.sprites[self.action]
        self.last = now
                
    def update(self):
        self.def_group()
        print(self.action,self.new_anim,self.is_running,self.is_jumping,self.is_slashing,self.is_blastering,self.current_sprite)
        self.animation()
        self.rect = self.image.get_rect()
        self.size = self.image.get_size()
        
        if self.action == "Sword" or self.action == "Blaster":
            self.offset = 128 - 96
        else:
            self.offset = 0
        if self.mirror:
            self.rect.center = (self.x - self.offset, self.y)
        else:
            self.rect.center = (self.x + self.offset, self.y)
        
    
    
    