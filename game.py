#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 22 11:08:56 2021

@author: marc
"""


import pygame
import time
from player import *
import menus

class MainLoop():
    
    def __init__(self):
        self.WIDTH, self.HEIGHT = 1920,1020
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.mouse = pygame.mouse.get_pos()
        self.main_menu = menus.Main_Menu(self.screen, self.WIDTH, self.HEIGHT)
        self.game_bg = pygame.transform.scale(pygame.image.load("Assets/ENVIRONMENT/background/skyline.png"), (750*3, 240*3)).convert_alpha()
        self.game_bg_rect = self.game_bg.get_rect()
        self.game_bg_size = self.game_bg.get_size()
        self.game_logo = menus.Game_Logo(self.screen,(self.WIDTH/2, self.HEIGHT*1/10))
        self.exit_menu = menus.Exit_Menu(self.screen, self.WIDTH, self.HEIGHT)
        self.settings_menu = menus.Settings_Menu(self.screen, self.WIDTH, self.HEIGHT)
        self.game_menu = menus.Game_Menu(self.screen, self.WIDTH, self.HEIGHT)
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
                            self.game_menu.running = False
                            self.game_running = False
                                   
            
            else:
                self.game_menu.manage_events(event1,self.main_menu,self.settings_menu,self.exit_menu,self.game_menu)             
        
    def manage_events(self,event):
        if self.game_menu.running == False:
            if event.type == pygame.QUIT:
                self.game_running = False
                self.running = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_menu.running = True
                
                if event.key == pygame.K_q or pygame.K_d or event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT or event.key == pygame.K_SPACE :
                    if self.player.is_jumping or self.player.is_slashing or self.player.is_blastering or self.player.is_running:
                        pass
                    else:
                        self.player.new_anim = True
                                                
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_q or event.key == pygame.K_LEFT\
                    or event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    self.player.is_running = False
                    print("test")
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0] :
                    if self.player.is_blastering or self.player.is_slashing:
                        pass
                    else:
                        self.player.new_anim = True
                        self.player.is_slashing = True
                
                    
                if pygame.mouse.get_pressed()[2]:
                    if self.player.is_slashing or self.player.is_blastering:
                        pass
                    else:
                        self.player.new_anim = True
                        self.player.is_blastering = True
                    
        
    def manage_pressed_keys(self):
        if self.game_menu.running == False:
            pressed_key = pygame.key.get_pressed()
            
            player_vector = [0,0]
            bg_vector = [0,0]
            
            if pressed_key[pygame.K_q] or pressed_key[pygame.K_LEFT]:
                if self.player.rect.center[0] <= self.WIDTH/2:
                    if self.game_bg_rect.left == 0:
                        if self.player.rect.left > 10:
                            player_vector[0] -= 1
                            bg_vector[0] = 0
                        
                    else:
                        player_vector[0] = 0
                        bg_vector[0] += 1
                        
                else:
                    if self.game_bg_rect.left == 0:
                        bg_vector[0] += 1
                        player_vector[0] = 0
                        
                    else:
                        player_vector[0] -= 1
                        bg_vector[0] = 0
                        
                
                self.player.mirror = True
                if self.player.is_slashing or self.player.is_blastering or self.player.is_jumping:
                    pass
                else:
                    if self.player.is_running:
                        pass
                    else:
                        self.player.is_running = True
                
                
    
            if pressed_key[pygame.K_d] or pressed_key[pygame.K_RIGHT]:
                if self.player.rect.center[0] < self.WIDTH/2:
                    if self.game_bg_rect.left == 0 :
                            player_vector[0] += 1
                            bg_vector[0] = 0
                            
                    else:
                        bg_vector[0] -= 0
                        player_vector[0] += 1
                        
                else:
                    if self.game_bg_rect.right > self.WIDTH:
                        bg_vector[0] -= 1
                        player_vector[0] = 0
                        
                    else:
                        if self.player.rect.right <= self.WIDTH - 10:
                            player_vector[0] += 1
                            bg_vector[0] = 0
                            

                self.player.mirror = False
                if self.player.is_slashing or self.player.is_blastering or self.player.is_jumping:
                    pass
                else:
                    self.player.is_running = True
                
                
            if pressed_key[pygame.K_SPACE]:
                print("is_jumping : ", self.player.is_jumping)
                if self.player.is_slashing or self.player.is_blastering:
                    pass
                else:
                    if self.player.is_jumping == False:
                        self.player.jump_sprite = 0
                        self.player.tick = self.clock.get_time()
                        self.player.y_origin = self.player.y
                        self.player.is_jumping = True
                        print("jump")
                    
                    
            if pygame.mouse.get_pressed()[0] :
                if self.player.is_blastering:
                    pass
                else:
                    self.player.is_slashing = True
                print("slash")
                
                    
            if pygame.mouse.get_pressed()[2]:
                if self.player.is_slashing:
                    pass
                else:
                    self.player.is_blastering = True
                
            if self.player.is_jumping or self.player.is_blastering or self.player.is_slashing:
                self.player.speed = 3
            else:
                self.player.speed = 10        
            self.player.move(player_vector)
            self.game_bg_move(bg_vector)
        
    def draw(self):
        if self.game_running:
            if self.game_bg_rect.left > 0:
                self.game_bg_rect.left = 0
            if self.game_bg_rect.left < self.WIDTH - self.game_bg_size[0]:
                self.game_bg_rect.left = self.WIDTH - self.game_bg_size[0]
            self.screen.blit(self.game_bg,(self.game_bg_rect[0],self.HEIGHT/2-self.game_bg_size[1]/2))
            self.screen.blit(self.player.image,self.player.rect)
            print(self.game_bg_rect[0],self.WIDTH - self.game_bg_size[0])
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
        self.game_bg_rect[0] = self.game_bg_rect[0] + deplacement[0]*self.player.speed
    

    def start(self):
        pygame.init()
        self.clock.tick(50)
        self.running = True
        while self.running:
            self.screen.blit(self.main_menu.menu_bg, (0,0))
            self.main_menu.menu_bg = self.main_menu.get_bg()
            self.game_logo.draw()
            self.main_menu.draw()
            pygame.display.update()
            mouse = pygame.mouse.get_pos()
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
        self.player = Player((self.WIDTH/2., self.HEIGHT/2.), 3, 1)
        self.screen.fill(0)
        pygame.display.update()
        time.sleep(0.5)
        while self.game_running:
            self.clock.tick(50)
            for event in pygame.event.get():
                self.manage_events(event)
            self.manage_pressed_keys()
            self.update()
        pygame.display.update()
            
            
    def quit(self):
        pygame.display.quit()
        pygame.quit()
        del self

        
            
            
            