import sys
import numpy as np
import pygame
import random
from Entity import Entity
from Bullet import Bullet

class Enemy(Entity):
    def __init__(self, pos, width, height, player):
        Entity.__init__(self, pos[0], pos[1], (random.randint(-12, 12), random.randint(-12, 12)), 3, (255, 255, 255), 27, width, height)
        if self.velocity[0] == 0:
            self.velocity = (self.velocity[0] + random.randint(1, 12), self.velocity[1])
        if self.velocity[1] == 0:
            self.velocity = (self.velocity[0], self.velocity[1] + random.randint(1, 12))
        self.player = player
        self.bullets = []
        self.fire = 0
        self.firerate = 25
    
    def update(self):
        Entity.update(self)
        if self.x < self.width/10:
            self.velocity[0] = -self.velocity[0]
        if self.x > self.width*9/10 - self.size:
            self.velocity[0] = -self.velocity[0]
        if self.y < self.size/10:
            self.velocity[1] = -self.velocity[1]
        if self.y > self.height*9/10 - self.size:
            self.velocity[1] = -self.velocity[1]
        self.fire += 1
        if self.fire == self.firerate:
            self.fire = 0
            target = (self.player.x - self.x, self.player.y - self.y)
            self.bullets.append( Bullet(self.x, self.y, target, self.player, self.width, self.height) )
        for bullet in self.bullets:
            bullet.update()
            if bullet.destroy:
                self.bullets.remove(bullet)

    def draw(self, screen):
        for bullet in self.bullets:
            bullet.draw(screen)