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
        self.player_vector = [0,0]

    
    def game_commands(self):
        if self.game:
            if self.paused == False:
                mouse = pygame.mouse.get_pos()
                pressed_key = pygame.key.get_pressed()
                self.player_vector = [0,0]

                

                if pressed_key[pygame.K_q] or pressed_key[pygame.K_LEFT]:
                    if self.loc_player[0] > 8:
                        self.left = True
                    else:
                        self.left = False
                else:
                    self.left = False

        
                if pressed_key[pygame.K_d] or pressed_key[pygame.K_RIGHT]:
                    if self.loc_player[0] < 632:
                        self.right = True
                    else:
                        self.right = False 
                else:
                    self.right = False   

                # if pressed_key[pygame.K_z] or pressed_key[pygame.K_UP]:
                #     if self.loc_player[1] > 8:
                #         self.up = True
                #     else:
                #         self.up = False  
                # else:
                #     self.up = False  

                # if pressed_key[pygame.K_s] or pressed_key[pygame.K_DOWN]:
                #     if self.loc_player[1] < 232:
                #         self.down = True
                #     else:
                #         self.down = False 
                # else:
                #     self.down = False   

                if pressed_key[pygame.K_SPACE]:
                    self.jump = True
                
                if self.left:
                    self.player_vector[0] -= 1
                if self.right:
                    self.player_vector[0] += 1
                # if self.up:
                #     self.player_vector[1] -= 1
                # if self.down:
                #     self.player_vector[1] += 1
                # for event in pygame.event.get():
                #     if event.type == pygame.KEYDOWN:
                #         if event.key == pygame.K_SPACE:
                #             self.jump = True

    def menu_commands(self):
        pass

    def exit_commands(self):
        pass

    def leave_command(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                del self
                sys.exit()
    
    def update(self):
        self.game_commands()
        self.menu_commands()
        self.exit_commands()
        self.leave_command()