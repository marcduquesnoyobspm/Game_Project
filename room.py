import pygame
import os
import numpy as np
from settings import DISPLAY, room_layout, floor_tile, wall_tile, corner_wall_tile, rock_tile, tile_size
from tile import Tile, Door

class Room(pygame.sprite.Sprite):

    def __init__(self, x, y, north, west, south, east):
        super().__init__()
        self.pos = [x,y]
        self.n_enemies = 0
        self.north = north
        self.west = west
        self.south = south
        self.east = east
        self.is_cleared = False
        self.room_layout = room_layout
        self.tile_size = tile_size
        self.room_tiles = pygame.sprite.Group()
        self.closed_doors = self.generate("closed_door")
        self.opened_doors = self.generate("opened_door")
    
    def generate(self, name):
        y = 0
        for row in self.room_layout:
            x = 0
            for tile in row:
                if tile == "1":
                    self.room_tiles.add(Tile(floor_tile, "N", x, y))
                if tile == "2":
                    if y == 0:
                        self.room_tiles.add(Tile(wall_tile, "N", x, y))
                    if y == 10:
                        self.room_tiles.add(Tile(wall_tile, "S", x, y))
                    if x == 0:
                        self.room_tiles.add(Tile(wall_tile, "W", x, y))
                    if x == 20:
                        self.room_tiles.add(Tile(wall_tile, "E", x, y))
                if tile == "3":
                    if y == 0:
                        if x == 0:
                            self.room_tiles.add(Tile(corner_wall_tile, "N", x, y))
                        if x == 20:
                            self.room_tiles.add(Tile(corner_wall_tile, "E", x, y))
                    if y == 10:                       
                        if x == 0:
                            self.room_tiles.add(Tile(corner_wall_tile, "W", x, y))
                        if x == 20:
                            self.room_tiles.add(Tile(corner_wall_tile, "S", x, y))
                if tile == "4":
                    if y == 0:
                        if self.north == False:
                            self.room_tiles.add(Tile(wall_tile, "N", x, y))
                    if y == 5:
                        if x == 0:
                            if self.west == False:
                                self.room_tiles.add(Tile(wall_tile, "W", x, y))
                        if x == 20:
                              if self.east == False:
                                self.room_tiles.add(Tile(wall_tile, "E", x, y))
                    if y == 10:
                        if self.south == False:
                            self.room_tiles.add(Tile(wall_tile, "S", x, y))
                if tile == "5":
                    self.room_tiles.add(Tile(rock_tile, "N", x, y))
                x += 1
            y += 1
        doors = pygame.sprite.Group()
        if self.north:
            doors.add(Door(name, "N", int(DISPLAY[0]/2), 0))
        if self.south:
            doors.add(Door(name, "S", int(DISPLAY[0]/2), DISPLAY[1]))
        if self.west:
            doors.add(Door(name, "W", 0, int(DISPLAY[1]/2)))
        if self.east:
            doors.add(Door(name, "E", DISPLAY[0], int(DISPLAY[1]/2)))
        return doors

    def pathfinding_layout(self):
        divide_number = 16
        multiplier_number = int(tile_size/divide_number)
        map = np.empty((int(DISPLAY[1]/divide_number), int(DISPLAY[0]/divide_number)))
        room_layout = np.array(self.room_layout)
        for x in range(room_layout.shape[0]):
            for y in range(room_layout.shape[1]):
                if self.room_layout[x][y] == "1":
                    map[x*multiplier_number : (x+1)*multiplier_number, y*multiplier_number : (y+1)*multiplier_number] = 0
                else:
                    map[x*multiplier_number : (x+1)*multiplier_number, y*multiplier_number : (y+1)*multiplier_number] = 1
        return map
        
    def is_room_cleared(self):
        if self.n_enemies == 0:
            self.is_cleared = True
        else:
            self.is_cleared = False
                                            
    def get_n_enemies(self, n_enemies):
        self.n_enemies = n_enemies
        
    def draw(self, surface):
        self.room_tiles.draw(surface)
        if self.is_cleared:
            self.opened_doors.draw(surface)
        else:
            self.closed_doors.draw(surface)


    def update(self, n_enemies):
        self.get_n_enemies(n_enemies)
        self.is_room_cleared()
