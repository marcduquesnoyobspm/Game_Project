#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 25 23:32:32 2021

@author: marc
"""

import time
import pygame
import numpy as np
import glob
import os
from main import *

pygame.init()

class Game_Logo():
    
    def __init__(self,screen,position):
        self.screen = screen
        self.x, self.y = position
        self.image = self.get_image()
        self.image = pygame.transform.scale(self.image,(509,312))
        self.image.set_colorkey([255,255,255])
        self.rect = self.image.get_rect()
        self.size = self.image.get_size()
        
    def get_image(self):
        image = pygame.image.load("Assets/test.gif").convert_alpha()
        image.set_colorkey((0,0,0))
        return image
    
    def draw(self):
        self.screen.blit(self.image,(self.x - self.size[0]/2, self.y))
        
        
class Button():
    
    def __init__(self,screen,name,position):
        self.screen = screen
        self.name = name
        self.x, self.y = position
        self.hovered = False
        self.image = self.get_image()
        self.size = self.image.get_size()
        self.rect = pygame.Rect(self.x - self.size[0]/2, self.y, self.size[0], self.size[1])

    def get_image(self):
        path = "Assets/Buttons/Large Buttons/Large Buttons/"+self.name+" Button.png"
        image = pygame.image.load(path).convert_alpha()
        if self.hovered:
            image.fill((255,255,150,255), None, pygame.BLEND_RGBA_MULT)
        else :
            image.fill((225,225,225,255), None, pygame.BLEND_RGBA_MULT)
        image = pygame.transform.scale(image, (120,40))
        self.size = image.get_size()
        self.rect = pygame.Rect(self.x - self.size[0]/2, self.y, self.size[0], self.size[1])
        return image
    
    def draw(self):
        self.screen.blit(self.image,(self.x - self.size[0]/2, self.y))
                 
                    

class Main_Menu():
    
    def __init__(self, screen, WIDTH, HEIGHT):
        self.running = True
        self.screen = screen
        self.WIDTH, self.HEIGHT = WIDTH, HEIGHT
        self.names = ["New game","Continue","Settings","Quit"]
        self.saved = False
        self.menu_bg_frames_paths = np.sort(glob.glob(os.path.abspath(os.getcwd()) + "/Assets/background/*.gif"))
        self.menu_bg_frames = [pygame.image.load(path).convert_alpha() for path in self.menu_bg_frames_paths]
        self.iteration = 0
        self.menu_bg = self.get_bg()
        self.new_game_button = Button(self.screen, "New game",(self.WIDTH/2, self.HEIGHT*3/5))
        self.continue_button = Button(self.screen, "Continue",(self.WIDTH/2, self.HEIGHT*3/5 + 50))
        self.settings_button = Button(self.screen, "Settings",(self.WIDTH/2, self.HEIGHT*3/5 + 100))
        self.quit_button = Button(self.screen, "Quit",(self.WIDTH/2, self.HEIGHT*3/5 + 150))
        self.buttons = [self.new_game_button, self.continue_button, self.settings_button, self.quit_button]
        
        
    def get_bg(self):
        menu_bg = self.menu_bg_frames[self.iteration]
        self.iteration += 1
        if self.iteration >= len(self.menu_bg_frames):
            self.iteration = 0
        return menu_bg
    
    def draw(self):
        for button in self.buttons:
            self.is_hovered(self.buttons)
            button.draw()
        
    
    def grey_continue(self):
        if self.saved == False:
            self.continue_button.image.fill((150,150,150,255), None, pygame.BLEND_RGBA_MULT)
            self.continue_button.hovered = False
            
            
    def is_hovered(self,menu_button):
        mouse = pygame.mouse.get_pos()
        for button in menu_button:
            if button.rect.collidepoint(mouse):
                button.hovered = True
                
            else:
                button.hovered = False
            button.image = button.get_image()
            self.grey_continue()
            
                
            
    def manage_events(self,event,main_menu,settings_menu,exit_menu,game_menu):
        mouse = pygame.mouse.get_pos()
        
        if event.type == pygame.QUIT:
            pygame.quit()
            
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_ESCAPE :
                exit_menu.running = True
                while exit_menu.running:
                    exit_menu.draw()
                    self.is_hovered(exit_menu.buttons)
                    for event1 in pygame.event.get():
                        exit_menu.manage_events(event1,main_menu,settings_menu,exit_menu,game_menu)
            if event.key == pygame.K_SPACE :
                self.saved = not(self.saved)
                
        if event.type == pygame.MOUSEBUTTONDOWN :
            if pygame.mouse.get_pressed()[0] :
                if self.quit_button.rect.collidepoint(mouse) :
                    exit_menu.running = True
                    while exit_menu.running:
                        exit_menu.draw()
                        self.is_hovered(exit_menu.buttons)
                        for event2 in pygame.event.get():
                            exit_menu.manage_events(event2,main_menu,settings_menu,exit_menu,game_menu)
                if self.settings_button.rect.collidepoint(mouse) :
                    settings_menu.running = True
                    while settings_menu.running:
                        settings_menu.draw()
                        self.is_hovered(settings_menu.buttons)
                        for event3 in pygame.event.get():
                            settings_menu.manage_events(event3,main_menu,settings_menu,exit_menu,game_menu)
                
                
    
class Exit_Menu():
    
    def __init__(self, screen, WIDTH, HEIGHT):
        self.running = False
        self.screen = screen
        self.WIDTH, self.HEIGHT = WIDTH, HEIGHT
        self.font = "NeonSans.ttf"
        self.color = "Pink"
        self.text = "Are you sure you want to quit ?"
        self.text_render, self.text_size, self.text_surface = self.get_text_params()
        self.bg_size = (self.text_size[0] + 100, self.HEIGHT/4.)
        self.quit_button = Button(self.screen, "Quit", (self.WIDTH/2 - self.bg_size[0]/4., self.HEIGHT/2. - self.bg_size[1]/2. + 100))
        self.back_button = Button(self.screen, "Back", (self.WIDTH/2 + self.bg_size[0]/4., self.HEIGHT/2. - self.bg_size[1]/2. + 100))
        self.bg_surface, self.bg_rect = self.get_bg_params()        
        self.buttons = [self.quit_button, self.back_button]
    
    def get_text_params(self):
        font_Font = pygame.font.Font("Assets/Fonts/"+self.font, 30)
        text_render = font_Font.render(self.text,1,self.color)
        text_size = text_render.get_size()
        text_size = text_size
        text_surface = pygame.Surface(text_size)  
        return text_render, text_size, text_surface
    
    def get_bg_params(self):
        bg_surface = pygame.Surface(self.bg_size)
        bg_rect = bg_surface.get_rect()
        bg_rect[0:2] = [self.WIDTH/2 - self.bg_size[0]/2., self.HEIGHT/2. - self.bg_size[1]/2.]        
        return bg_surface, bg_rect  
          
    def draw(self):
        pygame.draw.rect(self.screen, (255,255,255), self.bg_rect, width = 0, border_radius = 10) 
        pygame.draw.rect(self.screen, (0,0,0), self.bg_rect, width = 2, border_radius = 10)
        self.screen.blit(self.text_render,(self.WIDTH/2 - self.text_size[0]/2., self.HEIGHT/2. - self.bg_size[1]/2. + 20))
        self.screen.blit(self.quit_button.image,(self.WIDTH/2 - self.bg_size[0]/4 - self.quit_button.size[0]/2., self.HEIGHT/2. - self.bg_size[1]/2. + 100))
        self.screen.blit(self.back_button.image,(self.WIDTH/2 + self.bg_size[0]/4 - self.back_button.size[0]/2., self.HEIGHT/2. - self.bg_size[1]/2. + 100))
        pygame.display.update()
        
    def manage_events(self,event,main_menu,settings_menu,exit_menu,game_menu):
        mouse = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_ESCAPE :
                self.running = False

        if event.type == pygame.MOUSEBUTTONDOWN :
            if pygame.mouse.get_pressed()[0] :
                if self.quit_button.rect.collidepoint(mouse) :
                    self.running = False
                    pygame.quit()
                if self.back_button.rect.collidepoint(mouse) :
                    self.running = False
                
        
class Settings_Menu():
    
    def __init__(self, screen, WIDTH, HEIGHT):
        self.running = False
        self.screen = screen
        self.WIDTH, self.HEIGHT = WIDTH, HEIGHT
        self.font = "NeonSans.ttf"
        self.color = "Pink"
        self.title = "Settings"
        self.settings_menu = ["Brightness", "Volume", "Contrast", "Keybinds"]
        self.bg_size = (self.WIDTH/2., self.HEIGHT/2.)
        self.back_button = Button(self.screen, "Back", (self.WIDTH/2., self.HEIGHT/2. + self.bg_size[1]/3.))
        self.buttons = [self.back_button]
        self.title_render, self.title_size, self.title_surface = self.get_title_params()
        self.text_render, self.text_size, self.text_surface = self.get_text_params()
        self.bg_surface, self.bg_rect = self.get_bg_params()   
        
    def get_title_params(self):
        font_Font = pygame.font.Font("Assets/Fonts/"+self.font, 50)
        title_render = font_Font.render(self.title,1,self.color)
        title_size = title_render.get_size()
        title_surface = pygame.Surface(title_size)
        return title_render, title_size, title_surface
    
    def get_text_params(self):
        text_render = []
        text_size = []
        text_surface = []
        for item in self.settings_menu:
            font_Font = pygame.font.Font("Assets/Fonts/"+self.font, 30)
            item_text_render = font_Font.render(item,1,self.color)
            item_text_size = item_text_render.get_size()
            item_text_surface = pygame.Surface(item_text_size)
            text_render.append(item_text_render)
            text_size.append(item_text_size)
            text_surface.append(item_text_surface)
        return text_render, text_size, text_surface
        
    def get_bg_params(self):
        bg_surface = pygame.Surface(self.bg_size)
        bg_rect = bg_surface.get_rect()
        bg_rect[0:2] = [self.WIDTH/2 - self.bg_size[0]/2., self.HEIGHT/2. - self.bg_size[1]/2.]        
        return bg_surface, bg_rect  
    
    def draw(self):
        pygame.draw.rect(self.screen, (255,255,255), self.bg_rect, width = 0, border_radius = 10) 
        pygame.draw.rect(self.screen, (0,0,0), self.bg_rect, width = 2, border_radius = 10)
        self.screen.blit(self.back_button.image,(self.WIDTH/2. - self.back_button.size[0]/2., self.HEIGHT/2. + self.bg_size[1]/3.))
        self.screen.blit(self.title_render,(self.WIDTH/2. - self.title_size[0]/2., self.HEIGHT/2. - self.bg_size[1]/2. + 20))
        for render, size, surface, offset in zip(self.text_render, self.text_size, self.text_surface, range(len(self.text_render))):
            self.screen.blit(render,(self.WIDTH/2. - self.bg_size[0]/2. + 50, self.HEIGHT/2. - self.bg_size[1]/4. + offset*50))
        pygame.display.update()
        
    def manage_events(self,event,main_menu,settings_menu,exit_menu,game_menu):
        mouse = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_ESCAPE :
                self.running = False
                
        if event.type == pygame.MOUSEBUTTONDOWN :
            if pygame.mouse.get_pressed()[0] :
                if self.back_button.rect.collidepoint(mouse) :
                    self.running = False
                
        
class Game_Menu():
    
    def __init__(self, screen, WIDTH, HEIGHT):
        self.running = False
        self.screen = screen
        self.WIDTH, self.HEIGHT = WIDTH, HEIGHT
        self.font = "NeonSans.ttf"
        self.color = "Pink"
        self.title = "Pause"
        self.title_render, self.title_size, self.title_surface = self.get_title_params()
        self.bg_size = (self.title_size[0] + 20, self.title_size[1] + 220)
        self.names = ["Resume","Settings","Menu","Quit"]
        self.resume_button = Button(self.screen, "Resume",(self.WIDTH/2, self.HEIGHT/2 - self.bg_size[1]/2 + self.title_size[1] + 10))
        self.settings_button = Button(self.screen, "Settings",(self.WIDTH/2, self.HEIGHT/2 - self.bg_size[1]/2 + self.title_size[1] + 70))
        self.menu_button = Button(self.screen, "Menu",(self.WIDTH/2, self.HEIGHT/2 - self.bg_size[1]/2 + self.title_size[1] + 120))
        self.quit_button = Button(self.screen, "Quit",(self.WIDTH/2, self.HEIGHT/2 - self.bg_size[1]/2 + self.title_size[1] + 170))
        self.buttons = [self.resume_button, self.settings_button, self.menu_button, self.quit_button]
        self.bg_surface, self.bg_rect = self.get_bg_params() 
        
    def get_title_params(self):
        font_Font = pygame.font.Font("Assets/Fonts/"+self.font, 40)
        title_render = font_Font.render(self.title,1,self.color)
        title_size = title_render.get_size()
        title_surface = pygame.Surface(title_size)
        return title_render, title_size, title_surface

    def get_bg_params(self):
        bg_surface = pygame.Surface(self.bg_size)
        bg_rect = bg_surface.get_rect()
        bg_rect[0:2] = [self.WIDTH/2 - self.bg_size[0]/2., self.HEIGHT/2. - self.bg_size[1]/2.]        
        return bg_surface, bg_rect  
    
    def draw(self):
        pygame.draw.rect(self.screen, (255,255,255), self.bg_rect, width = 0, border_radius = 10) 
        pygame.draw.rect(self.screen, (0,0,0), self.bg_rect, width = 2, border_radius = 10)
        self.screen.blit(self.title_render,(self.WIDTH/2 - self.bg_size[0]/2 + 10, self.HEIGHT/2 - self.bg_size[1]/2))
        for button in self.buttons:
            button.draw()
        pygame.display.update()
        
    def manage_events(self,event,main_menu,settings_menu,exit_menu,game_menu):
        mouse = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            pygame.quit()
        
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

        if event.type == pygame.MOUSEBUTTONDOWN :
            
            if pygame.mouse.get_pressed()[0] :
                if self.resume_button.rect.collidepoint(mouse):
                    self.running = False 
                    time.sleep(0.2)
                if self.settings_button.rect.collidepoint(mouse):
                    settings_menu.running = True
                    while settings_menu.running:
                        settings_menu.draw()
                        main_menu.is_hovered(settings_menu.buttons)
                        for event1 in pygame.event.get():
                            settings_menu.manage_events(event1,main_menu,settings_menu,exit_menu,game_menu)                      
                    
                if self.quit_button.rect.collidepoint(mouse):
                    exit_menu.running = True
                    
                    while exit_menu.running:
                        exit_menu.draw()
                        main_menu.is_hovered(exit_menu.buttons)
                        for event3 in pygame.event.get():
                            exit_menu.manage_events(event3,main_menu,settings_menu,exit_menu,game_menu)
                    