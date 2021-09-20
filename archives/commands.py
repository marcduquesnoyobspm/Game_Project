import pygame
import sys

pygame.init()

class Commands():

    def __init__(self):
        self.loc_player = [0,0]
        self.menu = False
        self.game = False
        self.settings = False
        self.exit = False
        self.paused = False
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.jump = False
        self.attack = False
        self.events = None
        self.mirror = False
        self.player_vector = [0,0]

    def game_commands(self):
        if self.game:
            if self.paused:
                for event in self.events:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.paused = False
            else:
                mouse = pygame.mouse.get_pos()
                pressed_key = pygame.key.get_pressed()
                self.player_vector = [0,0]
                for event in self.events:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.paused = True

                if pressed_key[pygame.K_q]:
                    if self.attack:
                        pass
                    else:
                        self.mirror = True
                    if self.loc_player[0] > 8:
                        self.left = True
                    else:
                        self.left = False
                else:
                    self.left = False

                if pressed_key[pygame.K_d]:
                    if self.attack:
                        pass
                    else:
                        self.mirror = False
                    if self.loc_player[0] < 632:
                        self.right = True
                    else:
                        self.right = False 
                else:
                    self.right = False  

                if pressed_key[pygame.K_SPACE]:
                    self.jump = True

                if pressed_key[pygame.K_LEFT]:
                    if self.attack == False:
                        self.attack = True
                    else:
                        pass
                    self.mirror = True

                if pressed_key[pygame.K_RIGHT]:
                    if self.attack == False:
                        self.attack = True
                    else:
                        pass
                    self.mirror = False

                if self.attack:
                    pass
                else:
                    self.attack = False


                if self.left:
                    self.player_vector[0] -= 1
                if self.right:
                    self.player_vector[0] += 1

    def menu_commands(self):
        pass

    def exit_commands(self):
        pass
    
    def update(self):
        self.game_commands()
        self.menu_commands()
        self.exit_commands()