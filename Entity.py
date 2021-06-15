import sys
import numpy as np
import pygame

class Entity:
    def __init__(self, x, y, velocity, speed, color, size, width, height):
        self.x = x
        self.y = y
        self.velocity = velocity
        self.color = color
        self.size = size
        self.width = width
        self.height = height
        self.speed = speed

    def update(self):
        self.normalize()
        self.x += self.velocity[0] * self.speed
        self.y += self.velocity[1] * self.speed
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))

            
    def normalize(self):
        norm = np.linalg.norm(self.velocity)
        if norm != 0.0:
            self.velocity /= norm