#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 21 11:05:23 2021

@author: marc
"""

import pygame
import pytmx
import pyscroll

pygame.init()

screen = pygame.display.set_mode((1080,720))
menu = ["New Game","Continue","Options","Quit"]
caption = pygame.display.set_caption("Test du titre du jeu")
menu_bg = pygame.transform.scale(pygame.image.load("Assets/Background/single_background.png").convert(),(1080,720))

class Button() :
    
    def __init__(self,text,position,color,hovered) :
        self.x, self.y = position
        self.font = pygame.font.Font("Assets/Fonts/ARIAL.TTF",30)
        self.color = color
        self.text = self.font.render(text,1,color)
        self.size = self.text.get_size()
        self.surface = pygame.Surface(self.size)
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])
        self.rect[0] -= self.size[0]/2
        self.hovered = hovered
        
    def draw(self) :
        if self.hovered :
            pygame.draw.rect(screen,"Grey",self.rect)
            screen.blit(self.text,(self.x - self.size[0]/2, self.y))
        else :
            pygame.draw.rect(screen,"Black",self.rect)
            screen.blit(self.text,(self.x - self.size[0]/2, self.y))

def draw_text(screen,text,position,color) :
    x,y = position
    font = pygame.font.Font("Assets/Fonts/ARIAL.TTF",30)
    text = font.render(text,2,color)
    size = text.get_size()
    surface = pygame.Surface(size)
    rect = pygame.Rect(x, y, size[0], size[1])
    rect[0] = rect[0] - size[0]/2
    pygame.draw.rect(screen,"Black",rect)
    screen.blit(text,(x - size[0]/2, y))
    

def options() :
    running = True
    while running:
        mouse = pygame.mouse.get_pos()
        screen.blit(menu_bg, (0,0))
        draw_text(screen,"Options",(540,50),"White")
        luminosite = Button("Luminosité",(540,250),"White",hovered=False)
        contraste = Button("Contraste",(540,300),"White",hovered=False)
        test1 = Button("Test1",(540,350),"White",hovered=False)
        test2 = Button("Test2",(540,400),"White",hovered=False)
        test3 = Button("Test3",(540,450),"White",hovered=False)
        return_back = Button("Return",(540,500),"White",hovered=False)
        options_menu_buttons = [luminosite,contraste,test1,test2,test3,return_back]
        luminosite.draw()
        contraste.draw()
        test1.draw()
        test2.draw()
        test3.draw()
        return_back.draw()       
        for options_menu_button in options_menu_buttons :
            if options_menu_button.rect.collidepoint(mouse) :
                options_menu_button.hovered = True
                options_menu_button.draw()
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN :
                    if pygame.mouse.get_pressed()[0] :
                        if return_back.rect.collidepoint(mouse) :
                            running = False
            
        pygame.display.update()
    
    
def game() :
    running = True
    tmx_data = pytmx.util_pygame.load_pygame('map.tmx')
    map_data = pyscroll.data.TiledMapData(tmx_data)
    map_layer = pyscroll.orthographic.BufferedRenderer(map_data,screen.get_size())
    group = pyscroll.PyscrollGroup(map_layer=map_layer)
    while running:
        
        mouse = pygame.mouse.get_pos()
        group.draw(screen)
        pygame.display.update()
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                pygame.quit()
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_ESCAPE :
                    running = False
        
        
    
    
def run() :
    running = True
    while running :
        mouse = pygame.mouse.get_pos()
        screen.blit(menu_bg, (0,0))
        draw_text(screen,"Mon jeu",(540,50),"White")
        new_game_button = Button("New Game",(540,250),"White",hovered=False)
        load_button = Button("Continue",(540,300),"White",hovered=False)
        options_button = Button("Options",(540,350),"White",hovered=False)
        quit_button = Button("Quit",(540,400),"White",hovered=False)
        main_menu_buttons = [new_game_button,load_button,options_button,quit_button]
        new_game_button.draw()
        load_button.draw()
        options_button.draw()
        quit_button.draw()
        for main_menu_button in main_menu_buttons :
            if main_menu_button.rect.collidepoint(mouse) :
                main_menu_button.hovered = True
                main_menu_button.draw()
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN :
                    if pygame.mouse.get_pressed()[0] :
                        if quit_button.rect.collidepoint(mouse) :
                            running = False
                        if options_button.rect.collidepoint(mouse) :
                            options()
                        if new_game_button.rect.collidepoint(mouse) :
                            game()
        pygame.display.update()
    pygame.quit()

    


# def Main_Menu() :
    
#     def __init__(self,menu,color) :
#         self.menu = menu
#         self.new_game = Button("New Game",(540,150),"Black")
#         self.load = Button("Continue",(540,180),"Black")
#         self.options = Button("Options",(540,210),"Black")
#         self.quit = Button("Quit",(540,240),"Black")
    
#     def draw(self) :
#         self.new_game.draw()
#         self.load.draw()
#         self.options.draw()
#         self.quit.draw()
            
            



# class Title() :
    
#     def __init__(self,text,position,color) :
#         self.x, self.y = position
#         self.font = pygame.font.Font("Assets/Fonts/ARIAL.TTF",60)
#         self.color = color
#         self.text = self.font.render(text,2,self.color)
#         self.size = self.text.get_size()
#         self.surface = pygame.Surface(self.size)
#         self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])
        
#     def draw(self) :
#         screen.blit(self.text,(self.x - self.size[0]/2, self.y))
        
        
# class Options() :
    
#     def __init__(self) :
#         self.title = Title("Options",(540,50),"Black")
#         self.luminosite = Button("Luminosité",(540,150),"Black")
#         self.contraste = Button("Contraste",(540,150),"Black")
#         self.test1 = Button("Test1",(540,150),"Black")
#         self.test2 = Button("Test2",(540,150),"Black")
#         self.test3 = Button("Test3",(540,150),"Black")
#         self.returnback = Button("Return",(540,150),"Black")
        
#     def draw(self) :
#         self.title.draw()
#         self.luminosite.draw()
#         self.contraste.draw()
#         self.test1.draw()
#         self.test2.draw()
#         self.test3.draw()
#         self.returnback.draw()
