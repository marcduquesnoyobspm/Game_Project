#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 22 11:08:56 2021

@author: marc
"""


import pygame
import numpy as np
from player import *
from menus import *
from main import *


pygame.init()


class MainLoop():
    
    def __init__(self):
        self.WIDTH, self.HEIGHT = 1080,720
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.mouse = pygame.mouse.get_pos()
        self.main_menu = Main_Menu(self.screen, self.WIDTH, self.HEIGHT)
        self.main_menu_bg = self.main_menu.menu_bg
        self.game_bg = pygame.image.load("Assets/Background/medieval-15.jpg").convert_alpha()
        self.game_bg_rect = self.game_bg.get_rect()
        self.game_bg_size = self.game_bg.get_size()
        self.game_logo = Game_Logo(self.screen,(self.WIDTH/2, self.HEIGHT*1/10))
        self.exit_menu = Exit_Menu(self.screen, self.WIDTH, self.HEIGHT)
        self.settings_menu = Settings_Menu(self.screen, self.WIDTH, self.HEIGHT)
        self.game_menu = Game_Menu(self.screen, self.WIDTH, self.HEIGHT)
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_running = False
        self.player = Player((self.WIDTH/2., self.HEIGHT/2.), 3, 1)
        
    
    def is_hovered(self,button):
        mouse = pygame.mouse.get_pos()
        if button.rect.collidepoint(mouse):
            button.hovered = True
            self.main_menu.grey_continue()
        else:
            button.hovered = False
        button.image = button.get_image()
        button.draw()
        
    def game_menu_events(self):       
        self.main_menu.is_hovered(self.game_menu.buttons)
        for event1 in pygame.event.get():
            mouse = pygame.mouse.get_pos()
            if self.game_menu.menu_button.rect.collidepoint(mouse):
                if event1.type == pygame.MOUSEBUTTONDOWN :
                    if pygame.mouse.get_pressed()[0] :
                        if self.game_menu.menu_button.rect.collidepoint(mouse):
                            self.screen.fill(0)
                            pygame.display.update()
                            time.sleep(0.5)
                            self.game_menu.running = False
                            self.game_running = False
                            
            
            else:
                self.game_menu.manage_events(event1,self.main_menu,self.settings_menu,self.exit_menu,self.game_menu)             
        
    def manage_events(self,event):
        if self.game_menu.running == False:
            mouse = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                self.game_running = False
                self.running = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_menu.running = True
                
                if event.key == pygame.K_a or event.key == pygame.K_e or event.key == pygame.K_q or pygame.K_d \
                    or event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT or event.key == pygame.K_SPACE :
                    if self.player.is_jumping or self.player.is_slashing or self.player.is_blastering or self.player.is_running:
                        pass
                    else:
                        print("ok")
                        self.player.new_anim = True
                        
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_q or event.key == pygame.K_LEFT\
                    or event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    self.player.is_running = False
                

                    
        
    def manage_pressed_keys(self):
        if self.game_menu.running == False:
            pressed_key = pygame.key.get_pressed()
            
            player_vector = [0,0]
            bg_vector = [0,0]
            
            if pressed_key[pygame.K_q] or pressed_key[pygame.K_LEFT]:
                if self.player.rect.center[0] <= self.WIDTH/2:
                    if self.game_bg_rect.left == 0:
                        if self.player.rect.left > 20:
                            player_vector[0] -= 1
                    else:
                        bg_vector[0] += 1
                else:
                    if self.game_bg_rect.left == 0:
                        bg_vector[0] += 1
                    else:
                        player_vector[0] -= 1
                        
                if self.player.is_slashing or self.player.is_blastering or self.player.is_jumping:
                    pass
                else:
                    self.player.is_running = True
                
                
    
            if pressed_key[pygame.K_d] or pressed_key[pygame.K_RIGHT]:
                if self.player.rect.center[0] < self.WIDTH/2:
                    if self.game_bg_rect.left == 0 :
                            player_vector[0] += 1
                    else:
                        bg_vector[0] -= 1
                else:
                    if self.game_bg_rect.right  > self.WIDTH:
                        bg_vector[0] -= 1
                    else:
                        if self.player.rect.right < self.WIDTH - 20:
                            player_vector[0] += 1
                if self.player.is_slashing or self.player.is_blastering or self.player.is_jumping:
                    pass
                else:
                    self.player.is_running = True
                
                
            if pressed_key[pygame.K_SPACE]:
                if self.player.is_slashing or self.player.is_blastering:
                    pass
                else:
                    self.player.is_jumping = True
                    
            if pygame.mouse.get_pressed()[0] :
                if self.player.is_blastering:
                    pass
                else:
                    self.player.is_slashing = True
                
                    
            if pygame.mouse.get_pressed()[2]:
                if self.player.is_slashing:
                    pass
                else:
                    self.player.is_blastering = True
                
                    
            self.player.move(player_vector)
            self.game_bg_move(bg_vector)
        
    def draw(self):
        self.screen.blit(self.game_bg,self.game_bg_rect)
        self.screen.blit(self.player.image,self.player.rect)
        if self.game_menu.running:
            self.game_menu.draw()

    def update(self):
        if self.game_menu.running:
            self.game_menu_events()
        else:
            self.player.update()
        self.draw()
        pygame.display.update()
    
    def game_bg_move(self, deplacement):
        self.game_bg_rect[0], self.game_bg_rect[1] = self.game_bg_rect[0] + deplacement[0]*self.player.speed, self.game_bg_rect[1] + deplacement[1]*self.player.speed
    

    def start(self):
        self.running = True
        while self.running:
            mouse = pygame.mouse.get_pos()
            self.screen.blit(self.main_menu_bg, (0,0))
            self.game_logo.draw()
            self.main_menu.draw()
            for event in pygame.event.get():
                    self.main_menu.manage_events(event,self.main_menu,self.settings_menu,self.exit_menu,self.game_menu)
                    pygame.display.update()
                    if event.type == pygame.MOUSEBUTTONDOWN :
                        if pygame.mouse.get_pressed()[0] :
                            if self.main_menu.new_game_button.rect.collidepoint(mouse):
                                self.game_running = True
                                self.run()
        self.quit()
        
    def run(self):
        self.screen.fill(0)
        pygame.display.update()
        time.sleep(0.5)
        while self.game_running:
            self.clock.tick(60)
            self.update()
            for event in pygame.event.get():
                self.manage_events(event)
                self.update()
                pygame.display.update()
            self.manage_pressed_keys()
        pygame.display.update()
            
            
    def quit(self):
        pygame.display.quit()
        pygame.quit()
        del self

        
            
            
            