import pygame
import time
import sys
import os
from settings import RESOLUTION, DISPLAY
from level import Level

class Game():

    def __init__(self):
        self.screen = pygame.display.set_mode(RESOLUTION)
        self.display = pygame.Surface(DISPLAY)
        self.running = True
        self.level = Level(20)
        self.clock = pygame.time.Clock()
        self.reload_cd = 0
        self.is_game_over = False
        self.game_over_counter = 0        
        
    def reload(self, dt):
        pressed_key = pygame.key.get_pressed()
        if pressed_key[pygame.K_r]:
            self.reload_cd += dt
            if self.reload_cd >= 2:
                self.level = Level(20)
                self.reload_cd = 0
        else:
            self.reload_cd = 0
    
    def game_over(self):
        if self.level.player.sprites()[0].is_dead:
            self.is_game_over = True
        if self.is_game_over:
            text = "Game Over"
            font = pygame.font.Font(os.getcwd()+"/Assets/Fonts/Retro Gaming.ttf", 30)
            text_render = font.render(text,1,"Red")
            text_rect = text_render.get_rect()
            text_rect.center = (DISPLAY[0]/2,DISPLAY[1]/2)
            self.display.fill((0,0,0))
            self.display.blit(text_render,text_rect)
            self.game_over_counter += 1
        if self.game_over_counter >= 60*2:
            self.game_over_counter = 0
            self.level = Level(20)
            self.is_game_over = False
            
    def loading_screen(self):
        text = "Loading"
        font = pygame.font.Font(os.getcwd()+"/Assets/Fonts/Retro Gaming.ttf", 30)
        text_render = font.render(text,1,"Red")
        text_rect = text_render.get_rect()
        text_rect.center = (DISPLAY[0]/2,DISPLAY[1]/2)
        self.display.fill((0,0,0))
        self.display.blit(text_render,text_rect)
        self.screen.blit(pygame.transform.scale(self.display,RESOLUTION),(0,0))
        pygame.display.update()
                            
    def start(self):
            pygame.init()
            self.running = True
            self.run()

    def run(self):
        past_time = time.time()
        while self.running:
            now = time.time()
            dt = now - past_time
            past_time = now
            self.clock.tick(60)
            self.display.fill((0,0,0))
            self.reload(dt)
            while self.level.check_val == False:
                self.loading_screen()
                self.level.check_val, self.level.level_layout, self.level.rooms_group = self.level.check_level()
                self.level.current_room = self.level.get_current_room()
                self.level.enemies_group = self.level.generate_enemies()
                self.level.room_layout = self.level.current_room.pathfinding_layout()
            self.level.update(self.display, dt)
            self.game_over()
            self.screen.blit(pygame.transform.scale(self.display,RESOLUTION),(0,0))
            pygame.display.update()
            self.quit()
            
    def quit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.display.quit()
                pygame.quit()
                del self
                sys.exit()
