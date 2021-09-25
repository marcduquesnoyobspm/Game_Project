import pygame
import numpy as np
from pygame import surface
from room import Room
from player import Player
from bullet import Bullet
from enemy import Enemy
from settings import DISPLAY, tile_size
from hud import HUD
from pathfinding import astar


class Level():
    
    def __init__(self, nb_cells):
        self.layout_size = (11,11)
        self.nb_cells = nb_cells
        self.ending_rooms = 3
        self.total_enemies = 50
        self.start_cell = [int(self.layout_size[0]/2), int(self.layout_size[1]/2)]
        self.current_cell = self.start_cell.copy()
        self.check_val, self.level_layout, self.rooms_group = self.check_level()
        self.current_room = self.get_current_room()
        self.player = pygame.sprite.GroupSingle(Player(int(DISPLAY[0]/2), int(DISPLAY[1]/2), 3))
        self.enemies_group = self.generate_enemies()
        self.hud = HUD(self.level_layout, self.player.sprites()[0].health, self.player.sprites()[0].max_health)
        self.player_bullets = pygame.sprite.Group()
        self.room_layout = self.current_room.pathfinding_layout()
        
    def generate_level_layout(self):
        level_layout = np.zeros(self.layout_size)
        current_cell = [int(self.layout_size[0]/2), int(self.layout_size[1]/2)]
        level_layout[current_cell[0], current_cell[1]] = 1
        iteration = self.nb_cells * 2
        nb_cells = 1
        n = 0
        while n <= iteration and nb_cells < self.nb_cells:
            if current_cell[0] == 0:
                if current_cell[1] == 0:
                    direction = ["S", "E"]
                elif current_cell[1] == self.layout_size[1] - 1:
                    direction = ["W", "S"]
                else:
                    direction = ["W", "S", "E"]
            elif current_cell[0] == self.layout_size[0] - 1:
                if current_cell[1] == 0:
                    direction = ["N", "E"]
                elif current_cell[1] == self.layout_size[1] - 1:
                    direction = ["N", "W"]
                else:
                    direction = ["N", "W", "E"]
            else:
                if current_cell[1] == 0:
                    direction = ["N", "S", "E"]
                elif current_cell[1] == self.layout_size[1] - 1:
                    direction = ["N", "W", "S"]
                else:
                    direction = ["N", "W", "S", "E"]
            number = np.random.randint(0,len(direction))
            current_dir = direction[number]
            if current_dir == "N":
                current_cell[0] += -1
            elif current_dir == "W":
                current_cell[1] += -1
            elif current_dir == "S":
                current_cell[0] += 1
            elif current_dir == "E":
                current_cell[1] += 1
            level_layout[current_cell[0], current_cell[1]] = 1
            nb_cells = np.count_nonzero(level_layout == 1)
            n += 1
        return level_layout

    def check_level(self):
        level_layout = self.generate_level_layout()
        rooms_group = pygame.sprite.Group()
        ending_room = 0
        for x in range(level_layout.shape[0]):
            for y in range(level_layout.shape[1]):
                if level_layout[x, y] == 1:
                    north = False
                    south = False
                    west = False
                    east = False
                    if x > 0:
                        if level_layout[x - 1, y] == 1:
                            north = True
                    if x < level_layout.shape[0] - 1:
                        if level_layout[x + 1, y] == 1:
                            south = True
                    if y > 0:
                        if level_layout[x, y - 1] == 1:
                            west = True
                    if y < level_layout.shape[1] - 1:
                        if level_layout[x, y + 1] == 1:
                            east = True
                    doors = [north, south, west, east]
                    if doors.count(True) == 1:
                        ending_room += 1
                    rooms_group.add(Room(x, y, north, west, south, east))
        if ending_room >= self.ending_rooms:
            check_val = True
        else:
            check_val = False
        return check_val, level_layout, rooms_group
    
    def generate_enemies(self):
        enemies_group = pygame.sprite.Group()
        if self.current_room.is_cleared == False:
            
            if self.current_room.pos == self.start_cell:
                n_enemies = 0
            else:
                if self.total_enemies >= 10:
                    n_enemies = np.random.randint(0, 10)
                else:
                    n_enemies = np.random.randint(0, self.total_enemies)
            for n in range(n_enemies):
                enemies_group.add(Enemy("char_3", int(DISPLAY[0]/2) - (((n_enemies - 1)*40)/2) + n*40, int(DISPLAY[1]/2), 3, 0.5, 2))
        return enemies_group
    
    def get_current_room(self):
        for room in self.rooms_group:
            if room.pos == self.current_cell:
                current_room = room
        return current_room
    
    def doors_collisions(self):
        if self.current_room.is_cleared:
            player_sprite = self.player.sprites()[0].rect
            for door in self.current_room.opened_doors :
                if pygame.Rect.collidepoint(door.rect, player_sprite.midbottom):
                    if door.orientation == "N":
                        self.current_cell[0] += -1
                        player_sprite.midbottom = (int(DISPLAY[0]/2), DISPLAY[1] - 50) 
                    elif door.orientation == "W":
                        self.current_cell[1] += -1
                        player_sprite.bottomright = (DISPLAY[0] - 50, int(DISPLAY[1]/2))
                    elif door.orientation == "S":
                        self.current_cell[0] += 1
                        player_sprite.midtop = (int(DISPLAY[0]/2), 50) 
                    elif door.orientation == "E":
                        self.current_cell[1] += 1
                        player_sprite.bottomleft = (50, int(DISPLAY[1]/2))
                    self.current_room = self.get_current_room()
                    self.enemies_group = self.generate_enemies()                   
        
    def walls_collisions(self, point):
        hit_list = []
        for sprite in self.current_room.room_tiles:
            if sprite.name == "wall" or sprite.name == "rock":
                if pygame.Rect.collidepoint(sprite.rect, point):
                    hit_list.append(sprite)
        if self.current_room.is_cleared == False:
            for door in self.current_room.closed_doors:
                if pygame.Rect.collidepoint(door.rect, point):
                    hit_list.append(door)
        return hit_list
    
    def manage_player_bullets(self, dt):
        player_sprite = self.player.sprites()[0]
        if player_sprite.attack_cooldown <= 0:
            player_sprite.attack_cooldown = 0
        if player_sprite.attack_cooldown == 0:
            if player_sprite.is_shooting:
                player_sprite.attack_cooldown = 0.5
                player_sprite.is_shooting = False
                self.player_bullets.add(Bullet(player_sprite.rect.centerx, player_sprite.rect.centery, player_sprite.shoot, player_sprite.attack))
        else:
            player_sprite.attack_cooldown -= dt
        for bullet in self.player_bullets:
            if 0 > bullet.rect.right or bullet.rect.left > DISPLAY[0] or bullet.rect.bottom < 0 or bullet.rect.top > DISPLAY[1]:
                self.player_bullets.remove(bullet)
            for enemy in self.enemies_group:
                if enemy.rect.colliderect(bullet.rect):
                    enemy.health -= bullet.damage
                    self.player_bullets.remove(bullet)
                    
    def player_enemies_collisions(self, dt):
        player_sprite = self.player.sprites()[0]
        if player_sprite.is_vulnerable == False:
            if player_sprite.is_vulnerable_cooldown >= 1:
                player_sprite.is_vulnerable = True
                player_sprite.is_vulnerable_cooldown = 0
            else:
                player_sprite.is_vulnerable_cooldown += dt
        for enemy in self.enemies_group:
            if player_sprite.is_vulnerable:
                if player_sprite.rect.colliderect(enemy.rect):
                    player_sprite.health -= enemy.attack
                    player_sprite.is_vulnerable = False
        
                
    def manage_enemies(self, dt):
        if self.current_room.is_cleared == False:
            for enemy in self.enemies_group:
                if enemy.is_dead:
                    self.enemies_group.remove(enemy)
                if enemy.start_moving > 0.5:
                    enemy.direction = astar(self.room_layout, enemy.pos, self.player.sprites()[0].pos)
                else:
                    enemy.start_moving += dt
                    
    def update(self, surface, dt):
        self.current_room.update(len(self.enemies_group))
        self.current_room.draw(surface)

        self.doors_collisions()

        self.player.update(self.walls_collisions)
        self.player.draw(surface)
        
        self.manage_player_bullets(dt)
        self.player_bullets.update()
        self.player_bullets.draw(surface)
        
        self.manage_enemies(dt)
        self.enemies_group.update(self.walls_collisions)
        self.player_enemies_collisions(dt)
        self.enemies_group.draw(surface)
        
        self.hud.update(self.current_room, self.player.sprites()[0].health)
        self.hud.draw(surface, self.current_room, self.rooms_group)

        
        
        
