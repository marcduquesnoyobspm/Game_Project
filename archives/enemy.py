import pygame
import numpy as np

pygame.init()

class Enemy(pygame.sprite.Sprite):

    def __init__(self, name, x, y, health, attack):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.pos = x,y
        self.health_value = health
        self.attack_value = attack
        self.speed = 0.01
        self.speed_jump = -3
        self.move_vector = [0,0]
        self.y_momentum = 0
        self.air_timer = 0
        self.mirror = False
        self.is_jumping = False
        self.is_dead = False
        self.is_vulnerable = True
        self.invulnerability_counter = 0
        self.is_attacking = False
        self.knockback = 0
        self.sprite_attack_anim = 0
        self.mirror = False
        self.cooldown_attack = 0
        self.invulnerability_counter = 0
        self.image, self.size, self.rect_draw = self.get_image(name)
        self.rect = pygame.Rect(0,0,5,15)  
        self.rect.center = self.pos
        self.attack_hitbox = pygame.Rect(0,0,4,15)
    
    def get_image(self,name):
        image = pygame.image.load("Assets\Sprites\Own\Perso/" + name + ".png").convert()
        image.set_colorkey((0,0,0))
        if self.mirror:
            image = pygame.transform.flip(image, True, False)
        size = image.get_size()
        rect_draw = image.get_rect()
        return image, size, rect_draw

    def get_hit(self, damage):
        if self.is_vulnerable:
            self.health_value -= damage
            self.is_vulnerable = False

    def get_vulnerable(self):
        if self.is_vulnerable == False:
            self.invulnerability_counter += 1
            if self.invulnerability_counter >= 30:
                self.invulnerability_counter = 0
                self.is_vulnerable = True

    def collision_test(self,tiles_rects):
        hit_list = []
        for tile in tiles_rects:
            if self.rect.colliderect(tile):
                hit_list.append(tile)
        return hit_list
    
    def move(self, player_location, walls_rects, gravity):
        collision_types = {"Top" : False, "Bottom" : False, "Left" : False, "Right" : False}
        if 0 < (player_location[0] - self.rect.centerx - 4) * self.speed < 1:
            self.move_vector[0] = 1
        elif -1 < (player_location[0] - self.rect.centerx + 4) * self.speed < 0:
            self.move_vector[0] = -1
        else:
            self.move_vector[0] = np.rint((player_location[0] - self.rect.centerx) * self.speed)
        self.rect.centerx += self.move_vector[0]
        hit_list = self.collision_test(walls_rects)
        for tile in hit_list:
            if self.move_vector[0] > 0:
                self.rect.right = tile.left
                collision_types["Right"] = True
                self.is_jumping = True
            elif self.move_vector[0] < 0:
                self.rect.left = tile.right
                collision_types["Left"] = True
                self.is_jumping = True
        if player_location[1] < self.rect.centery or collision_types["Right"] or collision_types["Left"]:
            self.is_jumping = True
        else :
            self.is_jumping = False
        
        if self.is_jumping == False:
            self.move_vector[1] += gravity
            if self.move_vector[1] > 3:
                self.move_vector[1] = 3
        else:
            self.jump(gravity)
        self.rect.centery += self.move_vector[1]
        print(player_location[1], self.rect.centery, self.move_vector[1],self.is_jumping)
        hit_list = self.collision_test(walls_rects)
        for tile in hit_list:
            if self.move_vector[1] > 0:
                self.rect.bottom = tile.top
                collision_types["Bottom"] = True
                self.is_jumping = False
            elif self.move_vector[1] < 0:
                self.rect.top = tile.bottom
                self.move_vector[1] = 0
                collision_types["Top"] = True
        if collision_types["Bottom"]:
            self.move_vector[1] = 0
            self.air_timer = 0
            self.is_jumping = False
        else:
            self.air_timer += 1
            
    def jump(self, gravity):
        if self.is_jumping and self.air_timer == 0:
            self.move_vector[1] = self.speed_jump
        if self.is_jumping:
            self.move_vector[1] += gravity
            if self.move_vector[1] > 3:
                self.move_vector[1] = 3


    def death(self):
        if self.health_value <= 0 or self.rect_draw.top > 240:
            self.is_dead = True

    def attack(self):
        if self.is_attacking:
            pass
        else:
            if np.random.randint(0,120) == 0:
                self.is_attacking = True

    def hitbox(self):
        if self.is_attacking:
            if self.mirror:
                self.attack_hitbox.bottomright = self.rect.bottomleft
            else:
                self.attack_hitbox.bottomleft = self.rect.bottomright
    
    def draw(self,surface,scroll):
        percent_max_health_rect = pygame.Rect(self.rect.x,self.rect.y - 5,10,3)
        percent_max_health_rect[0] = self.rect.centerx - (10 - self.rect[2]) / 2 -1
        percent_player_health = self.health_value*10/3
        percent_player_health_rect = pygame.Rect(self.rect.x,self.rect.y - 5,int(percent_player_health),3)
        percent_player_health_rect[0] = percent_max_health_rect[0]
        pygame.draw.rect(surface, (255,0,0), (percent_player_health_rect[0] - scroll[0], percent_player_health_rect[1] - scroll[1], percent_player_health_rect[2], percent_player_health_rect[3]), width = 0, border_radius = 10)
        pygame.draw.rect(surface, (0,0,0), (percent_max_health_rect[0] - scroll[0], percent_max_health_rect[1] - scroll[1], percent_max_health_rect[2], percent_max_health_rect[3]), width = 1, border_radius = 10)
        if self.is_vulnerable == False:
            if 0 <= self.invulnerability_counter < 10 or 20 <= self.invulnerability_counter < 30:
                surface.blit(self.image,(self.rect_draw[0] - int(scroll[0]), self.rect_draw[1] - int(scroll[1])))
            else:
                pass
        else:    
            surface.blit(self.image, (self.rect_draw[0]  - int(scroll[0]), self.rect_draw[1] - int(scroll[1])))
            
    def update(self):
        self.pos = self.rect.center
        self.get_vulnerable()
        if self.is_vulnerable == False:
            if self.move_vector[0] == -1:
                self.knockback = 2
            else:
                self.knockback = -2
            self.rect.centerx += self.knockback
        else:
            self.knockback = 0
        if self.is_attacking:
            self.image, self.size, self.rect_draw = self.get_image(self.name + "_attack")
            if self.mirror:
                self.rect_draw.center = self.rect.center[0], self.rect.center[1]
            else:
                self.rect_draw.center = self.rect.center[0] + 1, self.rect.center[1]
        else:
            self.image, self.size, self.rect_draw = self.get_image(self.name)
            if self.mirror:
                self.rect_draw.center = self.rect.center[0], self.rect.center[1]
            else:
                self.rect_draw.center = self.rect.center[0] + 1, self.rect.center[1]
        
        self.attack()
        self.hitbox()
        self.death()