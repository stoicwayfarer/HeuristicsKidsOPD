import os
import pygame
import pyganim
from config import *


class CharacterAnimations:
    def __init__(self, character_name, size=(32, 32)):
        self.character_name = character_name
        self.size = size
        self.animations = {}
        self.current_animation = None
        self.facing_left = False
        self.image = pygame.Surface(size, pygame.SRCALPHA)
        self.rect = self.image.get_rect()

        # загрузка всех анимаций
        self.load_animations()

    def load_animations(self):
        base_path = os.path.join('assets', self.character_name)
        for animation_type in os.listdir(base_path):
            anim_path = os.path.join(base_path, animation_type)
            if os.path.isdir(anim_path):
                self.load_animation_frames(animation_type, anim_path)

    def load_animation_frames(self, animation_type, folder_path):
        frames = []

        # получаем все файлы изображений из папки
        image_files = sorted(
            [f for f in os.listdir(folder_path) if f.endswith(('.png', '.jpg', '.bmp'))]
        )

        for img_file in image_files:
            img_path = os.path.join(folder_path, img_file)
            frame = pygame.image.load(img_path).convert_alpha()
            frame = pygame.transform.scale(frame, self.size)
            frames.append((frame, max(ANIMATION_DELAY, 0.01)))

        if frames:
            anim = pyganim.PygAnimation(frames)
            anim.play()
            self.animations[animation_type] = anim

    def update_animation(self, state):
        self.image.fill((0, 0, 0, 0))

        animation_type = self.determine_animation_type(state)
        # анимация по умолочанию
        anim = self.animations.get(animation_type, self.animations.get('idle'))

        # проигрываем анимацию
        if anim:
            anim.blit(self.image, (0, 0))

        # отражение изображения если нужно
        if self.facing_left:
            self.image = pygame.transform.flip(self.image, True, False)

    # тип действия
    def determine_animation_type(self, state):
        if state.get('attacking', False):
            return 'attack'
        elif state.get('jumping', False):
            if not state.get('on_ground', True):
                if state.get('moving_left', False):
                    self.facing_left = True
                    return 'jump_left' if 'jump_left' in self.animations else 'jump'
                elif state.get('moving_right', False):
                    self.facing_left = False
                    return 'jump_right' if 'jump_right' in self.animations else 'jump'
                return 'jump'
        elif state.get('moving_left', False):
            self.facing_left = True
            return 'run'
        elif state.get('moving_right', False):
            self.facing_left = False
            return 'run'
        return 'idle'

    def get_image(self):
        return self.image