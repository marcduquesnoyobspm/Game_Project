import pygame
import numpy as np
from pygame import surface
from room import Room
from player import Player
from settings import DISPLAY


class Level():
    def __init__(self, nb_cells):
        self.layout_size = (11,11)
        self.nb_cells = nb_cells
        self.start_cell = [int(self.layout_size[0]/2), int(self.layout_size[1]/2)]
        self.current_cell = self.start_cell.copy()
        self.level_layout = self.generate_level_layout()
        self.player = pygame.sprite.GroupSingle(Player(int(DISPLAY[0]/2), int(DISPLAY[1]/2)))
        

    def generate_level_layout(self):
        level_layout = np.zeros(self.layout_size)
        current_cell = self.start_cell
        level_layout[current_cell[0], current_cell[1]] = 1
        iteration = self.nb_cells * 2
        nb_cells = 1 
        
        n = 0
        while n <= iteration and nb_cells < self.nb_cells:
            if current_cell[0] == 0:
                if current_cell[1] == 0:
                    direction = ["S", "E"]
                elif current_cell[1] == self.layout_size[1]:
                    direction = ["W", "S"]
                else:
                    direction = ["W", "S", "E"]

            elif current_cell[0] == self.layout_size[0]:
                if current_cell[1] == 0:
                    direction = ["N", "E"]
                elif current_cell[1] == self.layout_size[1]:
                    direction = ["N", "W"]
                else:
                    direction = ["N", "W", "E"]

            else:
                if current_cell[1] == 0:
                    direction = ["N", "S", "E"]
                elif current_cell[1] == self.layout_size[1]:
                    direction = ["N", "W", "S"]
                else:
                    direction = ["N", "W", "S", "E"]
               
            current_dir = direction[np.random.randint(0,len(direction) - 1)]
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

    def generate_room(self):
        north = False
        south = False
        west = False
        east = False
        
        if self.level_layout[self.current_cell[0] - 1, self.current_cell[1]] == 1:
            north = True
        if self.level_layout[self.current_cell[0] + 1, self.current_cell[1]] == 1:
            south = True
        if self.level_layout[self.current_cell[0], self.current_cell[1] - 1] == 1:
            west = True
        if self.level_layout[self.current_cell[0], self.current_cell[1] + 1] == 1:
            east = True
        self.room = Room(north, west, south, east)

    def doors_collisions(self):
        player_sprite = self.player.sprites()[0].rect
        for door_pos, door_rect in self.room.doors.items() :
            if player_sprite.colliderect(door_rect):
                if door_pos == "N":
                    self.current_cell[0] += -1
                    player_sprite.midbottom = (int(DISPLAY[0]/2), DISPLAY[1] - 50) 
                elif door_pos == "W":
                    self.current_cell[1] += -1
                    player_sprite.midright = (DISPLAY[0] - 50, int(DISPLAY[1]/2))
                elif door_pos == "S":
                    self.current_cell[0] += 1
                    player_sprite.midtop = (int(DISPLAY[0]/2), 50) 
                elif door_pos == "E":
                    self.current_cell[1] += 1
                    player_sprite.midleft = (50, int(DISPLAY[1]/2))
        
    def walls_collisions(self):
        hit_list = []
        for wall in self.room.room_tiles:
            if self.player.sprites()[0].rect.colliderect(wall):
                if pygame.Rect.collidepoint(wall.rect,self.player.sprites()[0].rect.midbottom):
                    hit_list.append(wall)
        return hit_list

        
                
 

    def run(self):
        pass

    def update(self, surface, dt):
        self.generate_room()

        self.room.update()
        self.room.draw(surface)

        self.doors_collisions()

        self.player.update(self.walls_collisions, dt)
        self.player.draw(surface)

        
        
        