import sys
import numpy as np
import pygame
import random
from Entity import Entity

class Bullet(Entity):
    def __init__(self, x, y, velocity, player, width, height):
        Entity.__init__(self, x, y, velocity, 3, (0, 0, 0), 9, width, height)
        self.player = player
        self.destroy = False  
    
    def update(self):
        Entity.update(self)
        if self.x < -self.size:
            self.destroy = True
        if self.x > self.width:
            self.destroy = True
        if self.y < -self.size:
            self.destroy = True
        if self.y > self.height:
            self.destroy = True
        if self.colliding(self.player):
            self.player.hit = True
        

    def colliding(self, player):
        if self.x + self.size >= player.x and self.x - self.size <= player.x and self.y + self.size >= player.y and self.y - self.size <= player.y:
            return True
        return False