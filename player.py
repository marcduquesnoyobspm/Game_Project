import pygame
import numpy as np
from settings import TARGET_FPS, DISPLAY

class Player(pygame.sprite.Sprite):

    def __init__(self,x , y):
        super().__init__()
        self.pos = [x, y]
        self.speed = 3
        self.moving = pygame.math.Vector2(0,0)
        self.direction = pygame.math.Vector2(0,0)
        self.image = pygame.image.load("Assets\Sprites\Own\Perso\char_3.png").convert_alpha()
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect(center = self.pos)
    
    def get_inputs(self):
        self.direction = pygame.math.Vector2(0,0)
        pressed_key = pygame.key.get_pressed()

        if pressed_key[pygame.K_q]:
            if self.rect.centerx <= 34:
                self.direction.x = 0
            else:
                self.direction.x += -1
        if pressed_key[pygame.K_d]:
            if self.rect.centerx >= 606:
                self.direction.x = 0
            else:
                self.direction.x += 1

        if pressed_key[pygame.K_z]:
            if self.rect.bottom <= 34:
                self.direction.y = 0
            else:
                self.direction.y += -1
        if pressed_key[pygame.K_s]:
            if self.rect.bottom >= 318:
                self.direction.y = 0
            else:
                self.direction.y += 1

    def move(self, collide_function, dt):
            collision_types = {"Top" : False, "Bottom" : False, "Left" : False, "Right" : False}
            
            lerp = pygame.math.Vector2.lerp(self.moving, self.direction, 0.2)
            self.moving = lerp
            if self.direction == [1,1] or self.direction == [-1, 1] or self.direction == [-1, -1] or self.direction == [1, -1]:
                norm = pygame.math.Vector2.length(self.direction)
            else:
                norm = 1
            if -0.2 < self.moving[0] < 0.2:
                self.speed = 0
            else:
                self.speed = 3
            if np.abs(self.moving[0]) > 0.99:
                self.moving[0] = np.round(self.moving[0])
            self.rect.centerx += 1/norm * self.moving[0] * self.speed
            print(self.rect.center, 1/norm, self.direction, self.moving[0] * self.speed, lerp)
            hit_list = collide_function()
            for tile in hit_list:
                if lerp[0] > 0:
                    self.rect.centerx = tile.rect.left - 2
                    lerp[0] = 0
                    self.moving[0]
                    collision_types["Right"] = True
                elif lerp[0] < 0:
                    self.rect.centerx = tile.rect.right + 2
                    lerp[0] = 0
                    self.moving[0]
                    collision_types["Left"] = True

            if -0.2 < lerp[1] < 0.2:
                self.speed = 0
            else:
                self.speed = 5
            self.rect.centery += 1/norm * self.moving[1] * self.speed
            hit_list = collide_function()
            for tile in hit_list:
                if lerp[1] > 0:
                    self.rect.bottom = tile.rect.top - 2
                    lerp[1] = 0
                    self.moving[1]
                    collision_types["Bottom"] = True
                elif lerp[1] < 0:
                    self.rect.bottom = tile.rect.bottom + 2
                    lerp[1] = 0
                    self.moving[1]
                    collision_types["Top"] = True
            

    

    def update(self, collide_function, dt):
        self.get_inputs()
        self.move(collide_function, dt)