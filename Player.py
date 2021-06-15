import sys
import numpy as np
import pygame
from Entity import Entity

class Player(Entity):
    def __init__(self, x, y, width, height):
        Entity.__init__(self, x, y, (0, 0), 3, (255, 0, 0), 9, width, height)
        self.hit = False
        self.xwall = False
        self.ywall = False
        self.averages = []
        for x in range(50):
            self.averages.append((self.x, self.y))

    def setVelocity(self, velocity):
        self.velocity = velocity

    def update(self):
        Entity.update(self)
        if self.x < 0:
            self.x = 0
            self.xwall = True
        if self.x > self.width - self.size:        
            self.x = self.width - self.size
            self.xwall = True
        if self.y < 0:       
            self.y = 0
            self.ywall = True
        if self.y > self.height - self.size:
            self.y = self.height - self.size
            self.ywall = True
        self.averages.pop(0)
        self.averages.append((self.x, self.y))

    def getAverageVelocity(self):
        v = (self.averages[len(self.averages) - 1][0] - self.averages[0][0], self.averages[len(self.averages) - 1][1] - self.averages[0][1])
        return np.linalg.norm(v)

    def getInput(self, enemies, inp):
        offset = self.size * (inp - 2)/2
        inputs = []
        inRange = []
        #Bullets in input space
        for enemy in enemies:
            for bullet in enemy.bullets:
                if self.x + self.size + offset >= bullet.x and self.x - self.size - offset <= bullet.x and self.y + self.size + offset >= bullet.y and self.y - self.size - offset <= bullet.y:
                    inRange.append(bullet)
        #Check locations
        for x in range(inp):
            px = self.x - offset + x * self.size
            for y in range(inp):
                py = self.y - offset + y * self.size
                i = 0
                for bullet in inRange:
                    if bullet.x + self.size >= px and bullet.x <= px and bullet.y + self.size >= py and bullet.y <= py:
                        v1 = [self.x - bullet.x, self.y - bullet.y]
                        v2 = [bullet.velocity[0], bullet.velocity[1]]
                        uv1 = v1 / np.linalg.norm(v1)
                        uv2 = v2 / np.linalg.norm(v2)
                        dot = np.dot(uv1, uv2)
                        if dot > 1:
                            dot = 1
                        if dot < -1:
                            dot = -1
                        angle = np.arccos(dot) * 180 / np.pi
                        if angle > 180:
                            angle = 360 - angle
                        v = -angle/180 + 1.0   
                        i = max(v, i)
                        inRange.remove(bullet)
                if i < 0.25:
                    if px < 0 or px > self.width or py < 0 or py > self.height:
                        i = 0.25
                inputs.append(i)
        return inputs
