import numpy as np
import glob
import os
from datetime import datetime
import time
import pygame

pygame.init()
WIDTH, HEIGHT = 380,720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
t = datetime.now()
print(t.second)
t = time.time_ns()//1000
t1 = time.time_ns()//1000 +1
print(t1 - t)
dir = os.path.abspath(os.getcwd())
test = np.sort(glob.glob(os.path.abspath(os.getcwd()) + "/Assets/background/*.gif"))
menu_bg_frames = [pygame.image.load(path).convert_alpha() for path in test]
print(len(menu_bg_frames))