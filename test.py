import numpy as np
import glob
import os
from datetime import datetime
import time
import sys
import pygame
import matplotlib.pyplot as plt
from settings import room_layout, DISPLAY, tile_size
from pathfinding import astar
pygame.init()

# def pathfinding_layout(room_layout):
#     map = np.array(room_layout)
#     for x in range(map.shape[0]):
#         for y in range(map.shape[1]):
#             if room_layout[x][y] == "1":
#                 map[x,y] = 0
#             else:
#                 map[x,y] = 1
#     return map
tile_size = 4
def pathfinding_layout(room_layout):
    map = np.empty((int(DISPLAY[1]/8), int(DISPLAY[0]/8)))
    room = np.array(room_layout)
    for x in range(room.shape[0]):
        for y in range(room.shape[1]):
            if room_layout[x][y] == "1":
                map[x*tile_size : (x+1)*tile_size, y*tile_size : (y+1)*tile_size] = 0
            else:
                map[x*tile_size : (x+1)*tile_size, y*tile_size : (y+1)*tile_size] = 1
    return map

maze = pathfinding_layout(room_layout)
start = (300,50)
end = (150,176)

path = astar(maze,start,end)

print(path)

plt.figure()
plt.imshow(maze)
plt.show()

    

