import pygame
import player
import commands
import menu
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
        self.clock = pygame.time.Clock()
        self.player = player.Player(216,88)
        self.commands = commands.Commands()
        self.camera = camera.Camera()
        self.game_map = self.load_map("map.txt")
        self.grass = pygame.image.load("Assets\Sprites\Own\Perso\Grass.png")
        self.dirt = pygame.image.load("Assets\Sprites\Own\Perso\Dirt.png")
        self.tile_size = 16
        self.air_timer = 0
        self.y_momentum = 0
        self.on_ground = True
        self.gravity = 0.2

    def load_map(self,path):
        f = open(path, 'r')
        data = f.read()
        f.close()
        data = data.split('\n')
        game_map = []
        for row in data:
            game_map.append(list(row))
        return game_map

    def collision_test(self):
        hit_list = []
        for tile in self.tile_rects:
            if self.player.collide_rect.colliderect(tile):
                hit_list.append(tile)
        return hit_list
    
    def move(self):
        collision_types = {"Top" : False, "Bottom" : False, "Left" : False, "Right" : False}
        self.player.collide_rect.x += self.player.speed * self.commands.player_vector[0]
        self.player.update()
        hit_list = self.collision_test()
        for tile in hit_list:
            if self.commands.player_vector[0] > 0:
                self.player.collide_rect.right = tile.left
                collision_types["Right"] = True
                print("right")
            elif self.commands.player_vector[0] < 0:
                self.player.collide_rect.left = tile.right
                collision_types["Left"] = True
                print("left")
        self.player.update()
        if self.commands.jump == False:
            self.y_momentum += self.gravity
            if self.y_momentum > 3:
                self.y_momentum = 3
        self.commands.player_vector[1] = self.y_momentum
        self.player.collide_rect.y += self.commands.player_vector[1]
        self.player.update()
        hit_list = self.collision_test()
        for tile in hit_list:
            if self.y_momentum > 0:
                self.player.collide_rect.bottom = tile.top
                collision_types["Bottom"] = True
                self.commands.jump = False
            elif self.y_momentum < 0:
                self.player.collide_rect.top = tile.bottom
                self.y_momentum = 0
                collision_types["Top"] = True
                print("top")
        self.player.update()
        if collision_types["Bottom"]:
            self.y_momentum = 0
            self.air_timer = 0
            self.commands.jump = False
        else:
            self.air_timer += 1
        
               
    def jump(self):
        if self.commands.jump and self.air_timer == 0:
            self.y_momentum = -5
        if self.commands.jump:
            self.y_momentum += self.gravity
            if self.y_momentum > 3:
                self.y_momentum = 3
            

    def draw_map(self):
        self.display.fill((146,244,255))
        y = 0
        self.tile_rects = []
        for row in self.game_map:
            x = 0
            for tile in row:
                if tile == "1":
                    self.display.blit(self.grass, (x * self.tile_size - int(self.camera.scroll[0]), y * self.tile_size - int(self.camera.scroll[1])))
                if tile == "2":
                    self.display.blit(self.dirt, (x * self.tile_size - int(self.camera.scroll[0]), y * self.tile_size - int(self.camera.scroll[1])))
                if tile != "0":
                    self.tile_rects.append(pygame.Rect(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size))
                x += 1
            y += 1
        
    def draw(self):
        self.display.blit(self.player.image,(self.player.rect[0] - int(self.camera.scroll[0]), self.player.rect[1] - int(self.camera.scroll[1])))
        pygame.draw.rect(self.display,(255,0,0),(self.player.collide_rect[0]  - int(self.camera.scroll[0]), self.player.collide_rect[1] - int(self.camera.scroll[1]), self.player.collide_rect[2], self.player.collide_rect[3]),width = 1)
        self.screen.blit(pygame.transform.scale(self.display,self.RESOLUTION),(0,0))

    def update(self):
        self.commands.loc_player = self.player.collide_rect.center
        self.commands.update()
        self.draw_map()
        self.jump()
        self.move()
        self.player.update()
        self.camera.loc_player = self.player.collide_rect.center
        self.camera.update()
        self.draw()

    def start(self):
        pygame.init()
        self.running = True
        self.run()

    def run(self):
        while self.running:
            self.clock.tick(60)
            self.commands.game = True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.update()
            pygame.display.update()
        self.quit()

    def quit(self):
        pygame.display.quit()
        pygame.quit()
        del self
        sys.exit()
    