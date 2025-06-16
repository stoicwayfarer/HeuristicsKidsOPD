import pygame
from config import *

class Camera:
    def __init__(self, width, height, world_width, world_height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.world_width = world_width
        self.world_height = world_height
        self.smooth_speed = 0.05 

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):
        target_x = -target.rect.centerx + self.width // 2
        target_y = -target.rect.centery + self.height // 2

        # границы
        target_x = min(0, target_x)
        target_x = max(-(self.world_width - self.width), target_x)
        target_y = min(0, target_y)
        target_y = max(-(self.world_height - self.height), target_y)

        self.camera.x += (target_x - self.camera.x) * self.smooth_speed
        self.camera.y += (target_y - self.camera.y) * self.smooth_speed
        
        self.camera.x = max(-(self.world_width - self.width), min(0, self.camera.x))
        self.camera.y = max(-(self.world_height - self.height), min(0, self.camera.y))