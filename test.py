import numpy as np
import glob
import os
from datetime import datetime
import time
import sys
import pygame

pygame.init()
WIDTH, HEIGHT = 160,160
screen = pygame.display.set_mode((WIDTH*3, HEIGHT*3))
display = pygame.Surface((WIDTH, HEIGHT))
dir = os.path.abspath(os.getcwd())
test = np.sort(glob.glob(os.path.abspath(os.getcwd()) + "/Assets/Sprites/Own/Perso/run*.png"))
menu_bg_frames = [pygame.image.load(path).convert_alpha() for path in test]
sprite_counter = 0
game_running = True
tile_size = 16
bg_rect = pygame.Rect(0,0,WIDTH/2,50)
ground_rect = pygame.Rect(WIDTH/3,HEIGHT/2,WIDTH/2,HEIGHT/3)
scroll = [0,0]

player_vector = [0,0]                    
while game_running:
    display.fill((22,19,40))
    clock = pygame.time.Clock()
    clock.tick(10)
    pressed_key = pygame.key.get_pressed()
    speed = 10 
      


    if sprite_counter >= len(menu_bg_frames):
        sprite_counter = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
            pygame.display.quit()
            pygame.quit()
            sys.exit()
    


    if pressed_key[pygame.K_q] or pressed_key[pygame.K_LEFT]:

        player_vector[0] -= 1

    if pressed_key[pygame.K_d] or pressed_key[pygame.K_RIGHT]:

        player_vector[0] += 1
    player = menu_bg_frames[sprite_counter]
    player_rect = player.get_rect()
    player_rect.center = (WIDTH/2 + player_vector[0]*speed, HEIGHT/2)
    scroll[0] += (player_rect.centerx - scroll[0] - 80)/10
    pygame.draw.rect(display,(255,255,255),(bg_rect[0]  - scroll[0]*0.25, bg_rect[1],bg_rect[2],bg_rect[3]))
    pygame.draw.rect(display,(25,25,155),(ground_rect[0] - scroll[0], ground_rect[1],ground_rect[2],ground_rect[3]))
    display_rect = display.get_rect()
    print(display_rect.left,player_rect.left,scroll[0])
    if display_rect.left == 0 or display.get_rect().right == screen.get_height():
        display.blit(player,player_rect.center)
        screen.blit(pygame.transform.scale(display,screen.get_size()),(0,0))
    else:
        player_rect.center = display.get_rect().center
        display.blit(player,player_rect.center)
        screen.blit(pygame.transform.scale(display,screen.get_size()),(0,0))
    sprite_counter += 1
    pygame.display.update()
pygame.display.quit()
pygame.quit()
sys.exit()

