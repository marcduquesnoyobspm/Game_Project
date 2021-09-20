import pygame

pygame.init()

class Player(pygame.sprite.Sprite):

    def __init__(self, x, y, health, attack):
        pygame.sprite.Sprite.__init__(self)
        self.name = "player"
        self.pos = x,y
        self.health_value = health
        self.attack_value = attack
        self.speed = 3
        self.speed_jump = -4
        self.move_vector = [0,0]
        self.y_momentum = 0
        self.air_timer = 0
        self.is_jumping = False
        self.is_attacking = False
        self.sprite_attack_anim = 0
        self.is_dead = False
        self.is_vulnerable = True
        self.mirror = False
        self.cooldown_attack = 0
        self.invulnerability_counter = 0
        self.image, self.size, self.rect_draw = self.get_image("char")
        self.rect = pygame.Rect(0,0,5,15)  
        self.rect.center = self.pos     
        self.attack_hitbox = pygame.Rect(0,0,10,15)
            
    
    def get_image(self,name):
        image = pygame.image.load("Assets\Sprites\Own\Perso/" + name + ".png").convert()
        image.set_colorkey((0,0,0))
        if self.mirror:
            image = pygame.transform.flip(image, True, False)
        size = image.get_size()
        rect_draw = image.get_rect()
        return image, size, rect_draw
    
    def get_hit(self,damage):
        if self.is_vulnerable:
            self.health_value -= damage
            self.is_vulnerable = False
    
    def get_vulnerable(self):
        if self.is_vulnerable == False:
            self.invulnerability_counter += 1
            if self.invulnerability_counter >= 2*60:
                self.invulnerability_counter = 0
                self.is_vulnerable = True

    def move(self, walls_rects, gravity):
        collision_types = {"Top" : False, "Bottom" : False, "Left" : False, "Right" : False}
        self.rect.x += self.speed * self.move_vector[0]
        hit_list = self.collision_test(walls_rects)
        for tile in hit_list:
            if self.move_vector[0] > 0:
                self.rect.right = tile.left
                collision_types["Right"] = True
            elif self.move_vector[0] < 0:
                self.rect.left = tile.right
                collision_types["Left"] = True
        if self.is_jumping == False:
            self.y_momentum += gravity
            if self.y_momentum > 3:
                self.y_momentum = 3
        self.move_vector[1] = self.y_momentum
        self.rect.y += self.move_vector[1]
        hit_list = self.collision_test(walls_rects)
        for tile in hit_list:
            if self.y_momentum > 0:
                self.rect.bottom = tile.top
                collision_types["Bottom"] = True
                self.is_jumping = False
            elif self.y_momentum < 0:
                self.rect.top = tile.bottom
                self.y_momentum = 0
                collision_types["Top"] = True
        if collision_types["Bottom"]:
            self.y_momentum = 0
            self.air_timer = 0
            self.is_jumping = False
        else:
            self.air_timer += 1
        self.pos = self.rect.center
    
    def jump(self, gravity):
        if self.is_jumping and self.air_timer == 0:
            self.y_momentum = self.speed_jump
        if self.is_jumping:
            self.y_momentum += gravity
            if self.y_momentum > 3:
                self.y_momentum = 3

    def collision_test(self,tiles_rects):
        hit_list = []
        for tile in tiles_rects:
            if self.rect.colliderect(tile):
                hit_list.append(tile)
        return hit_list
 
    def death(self):
        if self.health_value <= 0:
            self.is_dead = True

    def hitbox(self):
        if self.is_attacking:
            if self.mirror:
                self.attack_hitbox.bottomright = self.rect.bottomleft
            else:
                self.attack_hitbox.bottomleft = self.rect.bottomright

    def draw(self,surface,scroll):
        if self.is_vulnerable == False:
            if 0 <= self.invulnerability_counter < 10 or 20 <= self.invulnerability_counter < 30 or 40 <= self.invulnerability_counter < 50 \
                or 60 <= self.invulnerability_counter < 70 or 80 <= self.invulnerability_counter < 90 or 100 <= self.invulnerability_counter < 110:
                surface.blit(self.image,(self.rect_draw[0] - int(scroll[0]), self.rect_draw[1] - int(scroll[1])))
            else:
                pass
        else:
            surface.blit(self.image,(self.rect_draw[0] - int(scroll[0]), self.rect_draw[1] - int(scroll[1])))

    def update(self):
        self.pos = self.rect.center
        if self.is_attacking:
            self.image, self.size, self.rect_draw = self.get_image("char_attack")
            if self.mirror:
                self.rect_draw.center = self.rect.center[0] - 2, self.rect.center[1]
            else:
                self.rect_draw.center = self.rect.center[0] + 3, self.rect.center[1]
        else:
            self.image, self.size, self.rect_draw = self.get_image("char")
            if self.mirror:
                self.rect_draw.center = self.rect.center[0], self.rect.center[1]
            else:
                self.rect_draw.center = self.rect.center[0] + 1, self.rect.center[1]
        self.get_vulnerable()
        self.hitbox()
        self.death()
        
        
        
        
        