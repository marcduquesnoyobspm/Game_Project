import pygame

pygame.init()

class Camera():

    def __init__(self):
        self.loc_player = [320/2,160/2]
        self.lock_camera = pygame.Rect(0,0,320,160)
        self.x_locked = False
        self.y_locked = False
        self.scroll = [56,8]

    def locking(self):
        if (self.scroll[0] <= 0 and self.loc_player[0] < 160) or (self.scroll[0] >= 320 and self.loc_player[0] > 480):
            self.x_locked = True
        else:
            self.x_locked = False
        if (self.scroll[1] <= 0 and self.loc_player[1] < 80) or (self.scroll[1] >= 80 and self.loc_player[1] > 160):
            self.y_locked = True
        else:
            self.y_locked = False

    def scrolling(self):
        if self.x_locked == False:
            self.scroll[0] += ((self.loc_player[0] - self.scroll[0]) - self.lock_camera[2]/2) * 0.05
        else:
            if self.scroll[0] <= 0:
                self.scroll[0] = 0
            if self.scroll[0] >= 320:
                self.scroll[0] = 320
        if self.y_locked == False:
            self.scroll[1] += ((self.loc_player[1] - self.scroll[1]) - self.lock_camera[3]/2) *0.05
        else:
            if self.scroll[1] <= 0:
                self.scroll[1] = 0
            if self.scroll[1] >= 80:
                self.scroll[1] = 80
    
    def update(self):
        self.locking()
        self.scrolling()
        