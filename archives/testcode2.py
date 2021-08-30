#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 22 11:08:56 2021

@author: marc
"""


import pygame


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
        image = pygame.image.load("Assets/title.png")
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
        if self.hovered:
            path = "Assets/Buttons/Large Buttons/Colored Large Buttons/"+self.name+"  col_Button.png"
        else :
            path = "Assets/Buttons/Large Buttons/Large Buttons/"+self.name+" Button.png"
        image = pygame.image.load(path).convert_alpha()
        image.fill((255,255,255,190), None, pygame.BLEND_RGBA_MULT)
        image = pygame.transform.scale(image, (120,40))
        self.size = image.get_size()
        self.rect = pygame.Rect(self.x - self.size[0]/2, self.y, self.size[0], self.size[1])
        return image
    
    def draw(self):
        self.screen.blit(self.image,(self.x - self.size[0]/2, self.y))            
                    

class Main_Menu():
    
    def __init__(self, screen, WIDTH, HEIGHT):
        self.screen = screen
        self.WIDTH, self.HEIGHT = WIDTH, HEIGHT
        self.menu_buttons = ["New game","Continue","Settings","Quit"]
        self.saved = False
        self.menu_bg = self.get_bg()
        self.new_game_button = Button(self.screen, "New game",(self.WIDTH/2, self.HEIGHT*3/5))
        self.continue_button = Button(self.screen, "Continue",(self.WIDTH/2, self.HEIGHT*3/5 + 50))
        self.settings_button = Button(self.screen, "Settings",(self.WIDTH/2, self.HEIGHT*3/5 + 100))
        self.quit_button = Button(self.screen, "Quit",(self.WIDTH/2, self.HEIGHT*3/5 + 150))
        self.menu_buttons = [self.new_game_button, self.continue_button, self.settings_button, self.quit_button]
        
        
    def get_bg(self):
        menu_bg = pygame.transform.scale(pygame.image.load("Assets/Background/single_background.png").convert(),(self.WIDTH, self.HEIGHT))
        return menu_bg
    
    def draw(self):
        for button in self.menu_buttons:
            self.grey_continue()
            button.draw()
    
    def grey_continue(self):
        if self.saved == False:
            self.continue_button.image.fill((128,128,128,0), None, pygame.BLEND_RGBA_MULT)
            self.continue_button.hovered = False
            
    
    
class Exit_Menu():
    
    def __init__(self, screen, WIDTH, HEIGHT):
        self.screen = screen
        self.WIDTH, self.HEIGHT = WIDTH, HEIGHT
        self.font = "Retro Gaming.ttf"
        self.color = "black"
        self.text = "Are you sure you want to quit ?"
        self.text_render, self.text_size, self.text_surface = self.get_text_params()
        self.bg_size = (self.text_size[0] + 100, self.HEIGHT/4.)
        self.quit_button = Button(self.screen, "Quit", (self.WIDTH/2 - self.bg_size[0]/4., self.HEIGHT/2. - self.bg_size[1]/2. + 100))
        self.back_button = Button(self.screen, "Back", (self.WIDTH/2 + self.bg_size[0]/4., self.HEIGHT/2. - self.bg_size[1]/2. + 100))
        self.bg_surface, self.bg_rect = self.get_bg_params()        
        self.exit_menu_buttons = [self.quit_button, self.back_button]
    
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
        
        
class Settings_Menu():
    
    def __init__(self, screen, WIDTH, HEIGHT):
        self.screen = screen
        self.WIDTH, self.HEIGHT = WIDTH, HEIGHT
        self.font = "Retro Gaming.ttf"
        self.color = "black"
        self.title = "Settings"
        self.settings_menu = ["Brightness", "Volume", "Contrast", "Keybinds"]
        self.bg_size = (self.WIDTH/2., self.HEIGHT/2.)
        self.back_button = Button(self.screen, "Back", (self.WIDTH/2., self.HEIGHT/2. + self.bg_size[1]/3.))
        self.settings_menu_buttons = [self.back_button]
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
        
        
class MainLoop():
    
    def __init__(self):
        self.WIDTH, self.HEIGHT = 1080,720
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.main_menu = Main_Menu(self.screen, self.WIDTH, self.HEIGHT)
        self.main_menu_bg = self.main_menu.menu_bg
        self.game_logo = Game_Logo(self.screen,(self.WIDTH/2, self.HEIGHT*1/10))
        self.exit_menu = Exit_Menu(self.screen, self.WIDTH, self.HEIGHT)
        self.settings_menu = Settings_Menu(self.screen, self.WIDTH, self.HEIGHT)

    def is_hovered(self,button,mouse):
        if button.rect.collidepoint(mouse):
            button.hovered = True
            self.main_menu.grey_continue()
        else:
            button.hovered = False
        button.image = button.get_image()
        button.draw()
                        
    def run(self):
        running = True
        exit_val = False
        settings_val = False
        while running:
            mouse = pygame.mouse.get_pos()
            self.screen.blit(self.main_menu_bg, (0,0))
            self.game_logo.draw()
            self.main_menu.draw()
            self.main_menu.grey_continue()
            for button in self.main_menu.menu_buttons:
                self.is_hovered(button,mouse)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_ESCAPE :
                        exit_val = True
                    if event.key == pygame.K_SPACE :
                        self.main_menu.saved = True
                if event.type == pygame.MOUSEBUTTONDOWN :
                    if pygame.mouse.get_pressed()[0] :
                        if self.main_menu.quit_button.rect.collidepoint(mouse) :
                            exit_val = True
                        elif self.main_menu.settings_button.rect.collidepoint(mouse) :
                            settings_val = True
                            
            if exit_val == True:
                self.exit_menu.draw()
                while exit_val:
                    exit_mouse = pygame.mouse.get_pos()
                    for button in self.exit_menu.exit_menu_buttons:
                        self.is_hovered(button,exit_mouse)
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN :
                            if event.key == pygame.K_ESCAPE :
                                exit_val = False
                        if event.type == pygame.MOUSEBUTTONDOWN :
                            if pygame.mouse.get_pressed()[0] :
                                if self.exit_menu.quit_button.rect.collidepoint(exit_mouse) :
                                    running = False
                                    exit_val = False
                                if self.exit_menu.back_button.rect.collidepoint(exit_mouse) :
                                    exit_val = False
                        if event.type == pygame.QUIT:
                            running = False
                            exit_val = False
                    pygame.display.update()
                    
            if settings_val == True:
                self.settings_menu.draw()
                while settings_val:
                    settings_mouse = pygame.mouse.get_pos()
                    for button in self.settings_menu.settings_menu_buttons:
                        self.is_hovered(button,settings_mouse)
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN :
                            if pygame.mouse.get_pressed()[0] :
                                if self.settings_menu.back_button.rect.collidepoint(settings_mouse) :
                                    settings_val = False
                        if event.type == pygame.KEYDOWN :
                            if event.key == pygame.K_ESCAPE :
                                settings_val = False
                        if event.type == pygame.QUIT:
                            running = False
                            settings_val = False
                    pygame.display.update()
            
            pygame.display.update()
        pygame.quit()

game = MainLoop()
game.run()

        
            
            
            