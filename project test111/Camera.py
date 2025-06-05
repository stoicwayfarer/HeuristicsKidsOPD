import pygame
from config import *
class Camera:
    def __init__(self, width, height):
        self.camera_rect = pygame.Rect(0, WORLD_HEIGHT - SCREEN_HEIGHT, width, height)
        self.width = width
        self.height = height
        self.offset_x = 0
        self.offset_y = WORLD_HEIGHT-SCREEN_HEIGHT

    def apply(self, rect):
        return rect.move(-self.offset_x, -self.offset_y)

    def update(self, target):
        # Границы камеры
        border_left = self.camera_rect.left + self.width * CAMERA_BORDER_LEFT
        border_right = self.camera_rect.right - self.width * (1 - CAMERA_BORDER_RIGHT)
        border_top = self.camera_rect.top + self.height * CAMERA_BORDER_TOP
        border_bottom = self.camera_rect.bottom - self.height * (1 - CAMERA_BORDER_BOTTOM)

        # Горизонтальное движение камеры
        if target.rect.left < border_left:
            self.camera_rect.left = target.rect.left - self.width * CAMERA_BORDER_LEFT
        elif target.rect.right > border_right:
            self.camera_rect.right = target.rect.right + self.width * (1 - CAMERA_BORDER_RIGHT)

        # Вертикальное движение камеры
        if target.rect.top < border_top:
            self.camera_rect.top = target.rect.top - self.height * CAMERA_BORDER_TOP
        elif target.rect.bottom > border_bottom:
            self.camera_rect.bottom = target.rect.bottom + self.height * (1 - CAMERA_BORDER_BOTTOM)

        # Ограничиваем камеру границами мира
        if self.camera_rect.left < 0:
            self.camera_rect.left = 0
        if self.camera_rect.right > WORLD_WIDTH:
            self.camera_rect.right = WORLD_WIDTH
        if self.camera_rect.top < 0:
            self.camera_rect.top = 0
        if self.camera_rect.bottom > WORLD_HEIGHT:
            self.camera_rect.bottom = WORLD_HEIGHT

        self.offset_x = self.camera_rect.x
        self.offset_y = self.camera_rect.y