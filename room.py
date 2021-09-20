import pygame
from settings import DISPLAY, room_layout, wall_tile, corner_wall_tile, tile_size
from tile import Tile

class Room(pygame.sprite.Sprite):

    def __init__(self, north, west, south, east):
        super().__init__()
        self.north = north
        self.west = west
        self.south = south
        self.east = east
        self.door_image = pygame.image.load("Assets\Sprites\Own\Perso\door.png").convert_alpha()
        self.rect = self.door_image.get_rect()
        self.room_layout = room_layout
        self.tile_size = tile_size
        self.room_tiles = pygame.sprite.Group()
        self.doors = self.generate()
        
    
    def generate(self):
        y = 0
        for row in self.room_layout:
            x = 0
            for tile in row:
                if tile == "1":
                    self.room_tiles.add(Tile(wall_tile, x, y))
                if tile == "2":
                    self.room_tiles.add(Tile(corner_wall_tile, x, y))
                if tile == "3":
                    if y == 0:
                        if self.north == False:
                            self.room_tiles.add(Tile(wall_tile, x, y))
                    if y == 5:
                        if x == 0:
                            if self.west == False:
                                self.room_tiles.add(Tile(wall_tile, x, y))
                        if x == 20:
                             if self.east == False:
                                self.room_tiles.add(Tile(wall_tile, x, y))
                    if y == 10:
                        if self.south == False:
                            self.room_tiles.add(Tile(wall_tile, x, y))
                x += 1
            y += 1

        doors = {}
        if self.north:
            rect_north_door = pygame.Rect(0, 0, self.rect[2], self.rect[3])
            rect_north_door.midtop = (int(DISPLAY[0]/2), 0)
            doors["N"] = rect_north_door
        if self.south:
            rect_south_door = pygame.Rect(0, 0, self.rect[2], self.rect[3])
            rect_south_door.midbottom = (int(DISPLAY[0]/2), DISPLAY[1])
            doors["S"] = rect_south_door
        if self.west:
            rect_west_door = pygame.Rect(0, 0, self.rect[2], self.rect[3])
            rect_west_door.midleft = (0, int(DISPLAY[1]/2))
            doors["W"] = rect_west_door
        if self.east:
            rect_east_door = pygame.Rect(0, 0, self.rect[2], self.rect[3])
            rect_east_door.midright = (DISPLAY[0], int(DISPLAY[1]/2))
            doors["E"] = rect_east_door
        return doors

    def draw(self, surface):
        self.room_tiles.draw(surface)
        for door in self.doors.values():
            surface.blit(self.door_image, door)

    def update(self):
        self.doors = self.generate()