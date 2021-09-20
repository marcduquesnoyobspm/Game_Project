import pygame
import player
import commands
import menu
import gui
import enemy
import camera
import sys

class Game():

    def __init__(self):
        self.RESOLUTION = [1280,640]
        self.screen = pygame.display.set_mode(self.RESOLUTION)
        self.display = pygame.Surface((320,160))
        self.display_rect = self.display.get_rect()
        self.running = False
        self.is_game_over = False
        self.game_over_counter = 0
        self.gravity = 0.2
        self.clock = pygame.time.Clock()
        self.gui = gui.GUI()
        self.player = player.Player(216, 88, 3, 1)
        self.player_group = pygame.sprite.Group()
        self.player_group.add(self.player)
        self.commands = commands.Commands()
        self.camera = camera.Camera()
        self.game_map = self.load_map("map.txt")
        self.grass = pygame.image.load("Assets\Sprites\Own\Perso\Grass.png")
        self.dirt = pygame.image.load("Assets\Sprites\Own\Perso\Dirt.png")
        self.tile_size = 16
        self.walls_rects = self.get_walls_rects()
        self.level = 1
        self.enemies_group = self.load_enemies(self.level, 10, 0)
        

    def load_map(self,path):
        f = open(path, 'r')
        data = f.read()
        f.close()
        data = data.split('\n')
        game_map = []
        for row in data:
            game_map.append(list(row))
        return game_map

    def get_walls_rects(self):
        walls_rects = []
        y = 0
        for row in self.game_map:
            x = 0
            for tile in row:
                if tile != "0":
                    walls_rects.append(pygame.Rect(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size))
                x += 1
            y += 1
        return walls_rects
        
    def get_events(self):
        self.events = pygame.event.get()
    
    def game_over(self):
        if self.player.rect_draw.top > len(self.game_map) * self.tile_size or self.player.is_dead:
            self.is_game_over = True
        if self.game_over_counter >= 60*2:
            self.game_over_counter = 0
            self.level = 1
            self.player_group.remove(self.player)
            self.player = player.Player(216, 88, 3, 1)
            self.player_group.add(self.player)
            self.commands = commands.Commands()
            self.camera = camera.Camera()
            self.enemies_group = self.load_enemies(self.level, 10, 0)
            self.is_game_over = False

    def load_enemies(self,number,x,y):
        enemies_group = pygame.sprite.Group()
        for n in range(number):
            n_enemy = enemy.Enemy("enemy", 280 + n*x, 88 + n*y, 3, 0.5)
            enemies_group.add(n_enemy)
        return enemies_group

    def collision_test(self,entity_hitbox,tiles_rects):
        hit_list = []
        for tile in tiles_rects:
            if entity_hitbox.colliderect(tile):
                hit_list.append(tile)
                print(entity_hitbox,tile,"ok1")
        return hit_list
    
    def collision_enemy(self,enemies_group):
        for enemy_sprite in enemies_group:
            hit = pygame.sprite.collide_rect(self.player,enemy_sprite)
            if hit:
                self.player.get_hit(enemy_sprite.attack_value)

    def attack(self,attackers, targets):
        for attacker in attackers:
            if attacker.cooldown_attack == 0:
                if attacker.is_attacking:
                    attacker.sprite_attack_anim += 1
                    for enemy_sprite in targets:
                            if attacker.attack_hitbox.colliderect(enemy_sprite.rect):
                                enemy_sprite.get_hit(attacker.attack_value)
                    if attacker.sprite_attack_anim >= 60:
                        attacker.is_attacking = False
                        if attacker.name == "player":
                            self.commands.attack = False
                        attacker.cooldown_attack = 15
                if attacker.cooldown_attack > 0:
                    attacker.is_attacking = False
                    if attacker.name == "player":
                        self.commands.attack = False
            if attacker.cooldown_attack > 0:
                attacker.is_attacking = False
                if attacker.name == "player":
                    self.commands.attack = False
            if attacker.is_attacking == False:
                if attacker.sprite_attack_anim >= 60:
                    attacker.cooldown_attack = 15
                    attacker.sprite_attack_anim = 0                    
                elif attacker.cooldown_attack <= 0:
                    attacker.cooldown_attack = 0
                else:
                    attacker.cooldown_attack -= 1
            

        
  
    def move(self):
        collision_types = {"Top" : False, "Bottom" : False, "Left" : False, "Right" : False}
        self.player.rect.x += self.player.speed * self.player.move_vector[0]
        self.player.mirror = self.commands.mirror
        hit_list = self.collision_test(self.player.rect,self.walls_rects)
        for tile in hit_list:
            if self.player.move_vector[0] > 0:
                self.player.rect.right = tile.left
                collision_types["Right"] = True
            elif self.player.move_vector[0] < 0:
                self.player.rect.left = tile.right
                collision_types["Left"] = True
        if self.player.is_jumping == False:
            self.player.y_momentum += self.gravity
            if self.player.y_momentum > 3:
                self.player.y_momentum = 3
        self.player.move_vector[1] = self.player.y_momentum
        self.player.rect.y += self.player.move_vector[1]
        hit_list = self.collision_test(self.player.rect,self.walls_rects)
        for tile in hit_list:
            if self.player.y_momentum > 0:
                self.player.rect.bottom = tile.top
                collision_types["Bottom"] = True
                self.player.is_jumping = False
            elif self.player.y_momentum < 0:
                self.player.rect.top = tile.bottom
                self.player.y_momentum = 0
                collision_types["Top"] = True
        if collision_types["Bottom"]:
            self.player.y_momentum = 0
            self.player.air_timer = 0
            self.player.is_jumping = False
        else:
            self.player.air_timer += 1

        collision_types = {"Top" : False, "Bottom" : False, "Left" : False, "Right" : False}
        
        for enemy_sprite in self.enemies_group:
            if self.player.rect.centerx + 4 < enemy_sprite.rect.centerx:
                enemy_sprite.move_vector[0] = -1
                enemy_sprite.mirror = True
            elif self.player.rect.centerx - 4 > enemy_sprite.rect.centerx:
                enemy_sprite.move_vector[0] = 1
                enemy_sprite.mirror = False
            else:
                enemy_sprite.move_vector[0] = 0
            enemy_sprite.rect.x += enemy_sprite.speed*enemy_sprite.move_vector[0]
            hit_list = self.collision_test(enemy_sprite.rect,self.walls_rects)
            for tile in hit_list:
                if enemy_sprite.move_vector[0] > 0:
                    enemy_sprite.rect.right = tile.left
                elif enemy_sprite.move_vector[0] < 0:
                    enemy_sprite.rect.left = tile.right

            enemy_sprite.y_momentum += self.gravity
            print(enemy_sprite.rect,enemy_sprite.y_momentum,"ok")
            if enemy_sprite.y_momentum > 3:
                enemy_sprite.y_momentum = 3
            # enemy_sprite.move_vector[1] = enemy_sprite.y_momentum
            enemy_sprite.rect.y += enemy_sprite.y_momentum
            
            hit_list = self.collision_test(enemy_sprite.rect,self.walls_rects)
            for tile in hit_list:
                print(enemy_sprite.rect,enemy_sprite.y_momentum,"ok2")
                if enemy_sprite.y_momentum > 0:
                    print(enemy_sprite.rect,enemy_sprite.y_momentum,"ok3")
                    enemy_sprite.rect.bottom = tile.top
                    collision_types["Bottom"] = True
                    enemy_sprite.is_jumping = False
                elif enemy_sprite.y_momentum < 0:
                    enemy_sprite.rect.top = tile.bottom
                    enemy_sprite.y_momentum = 0
                    collision_types["Top"] = True
            # print(collision_types["Bottom"],enemy_sprite.y_momentum)
            if collision_types["Bottom"]:
                
                enemy_sprite.y_momentum = 0
                enemy_sprite.air_timer = 0
                enemy_sprite.is_jumping = False
                
            else:
                enemy_sprite.air_timer += 1
            

    def jump(self,entity):
        if entity.is_jumping and entity.air_timer == 0:
            entity.y_momentum = entity.speed_jump
        if entity.is_jumping:
            entity.y_momentum += self.gravity
            if entity.y_momentum > 3:
                entity.y_momentum = 3
                
    def draw(self):
        self.display.fill((146,244,255))
        y = 0
        for row in self.game_map:
            x = 0
            for tile in row:
                if tile == "1":
                    self.display.blit(self.grass, (x * self.tile_size - int(self.camera.scroll[0]), y * self.tile_size - int(self.camera.scroll[1])))
                if tile == "2":
                    self.display.blit(self.dirt, (x * self.tile_size - int(self.camera.scroll[0]), y * self.tile_size - int(self.camera.scroll[1])))
                x += 1
            y += 1
        self.player.draw(self.display,self.camera.scroll)
        # pygame.draw.rect(self.display,(0,255,0),(self.player.rect_draw[0]  - int(self.camera.scroll[0]), self.player.rect_draw[1] - int(self.camera.scroll[1]), self.player.rect_draw[2], self.player.rect_draw[3]),width = 1)
        # pygame.draw.rect(self.display,(0,255,0),(self.player.rect[0]  - int(self.camera.scroll[0]), self.player.rect[1] - int(self.camera.scroll[1]), self.player.rect[2], self.player.rect[3]))
        # if self.player.is_attacking:
        #     pygame.draw.rect(self.display,(0,0,255),(self.player.attack_hitbox[0]  - int(self.camera.scroll[0]), self.player.attack_hitbox[1] - int(self.camera.scroll[1]), self.player.attack_hitbox[2], self.player.attack_hitbox[3]),width = 1)
        for sprite in self.enemies_group:
            sprite.draw(self.display,self.camera.scroll)
            # pygame.draw.rect(self.display,(255,0,0),(sprite.rect[0]  - int(self.camera.scroll[0]), sprite.rect[1] - int(self.camera.scroll[1]), sprite.rect[2], sprite.rect[3]),width = 1)
        # self.gui.draw(self.display)
        self.gui.draw(self.display)
        if self.is_game_over:
            text = "Game Over"
            font = pygame.font.Font("Assets/Fonts/Retro Gaming.ttf", 30)
            text_render = font.render(text,1,"Red")
            text_rect = text_render.get_rect()
            text_rect.center = (self.display.get_size()[0]/2,self.display.get_size()[1]/2)
            self.display.fill((0,0,0))
            self.display.blit(text_render,text_rect)
            self.game_over_counter += 1
        self.screen.blit(pygame.transform.scale(self.display,self.RESOLUTION),(0,0))

    def update(self):
        if self.is_game_over == False:
            self.get_events()
            self.commands.events = self.events
            self.commands.loc_player = self.player.rect.center
            self.commands.update()
            if self.commands.paused == False:
                self.player.is_jumping = self.commands.jump
                self.player.move_vector = self.commands.player_vector
                self.player.mirror = self.commands.mirror
                if self.player.sprite_attack_anim == 0:
                    self.player.is_attacking = self.commands.attack
                self.player.jump(self.gravity)
                self.player.move(self.walls_rects,self.gravity)
                for enemy_sprite in self.enemies_group:
                    enemy_sprite.move(self.player.pos, self.walls_rects, self.gravity)
                self.collision_enemy(self.enemies_group)
                self.attack(self.player_group,self.enemies_group)
                self.attack(self.enemies_group,self.player_group)
                self.player.update()
                self.enemies_group.update()
                for enemy_sprite in self.enemies_group:
                    if enemy_sprite.is_dead:
                        self.enemies_group.remove(enemy_sprite)
                self.commands.jump = self.player.is_jumping
                self.camera.loc_player = self.player.rect.center
                self.camera.update()
                self.gui.update(self.player.health_value)
        self.game_over()
        self.draw()

    def start(self):
        pygame.init()
        self.running = True
        self.run()

    def run(self):
        while self.running:
            self.clock.tick(60)
            self.commands.game = True
            if len(self.enemies_group) == 0:
                self.level += 1
                self.enemies_group = self.load_enemies(self.level, 10, 0)
            self.update()
            pygame.display.update()
            self.quit()
            
    def quit(self):
        for event in self.events:
            if event.type == pygame.QUIT:
                self.running = False
                pygame.display.quit()
                pygame.quit()
                del self
                sys.exit()
    