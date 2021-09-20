import pygame
import time
import sys
from settings import RESOLUTION, DISPLAY
from level import Level

class Game():

    def __init__(self):
        self.screen = pygame.display.set_mode(RESOLUTION)
        self.display = pygame.Surface(DISPLAY)
        self.running = True
        self.level = Level(6)
        self.clock = pygame.time.Clock()

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
            self.level.update(self.display, dt)
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