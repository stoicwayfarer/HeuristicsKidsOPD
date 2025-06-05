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
        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect()
        
        # Загрузка всех анимаций
        self.load_animations()
        
    def load_animations(self):
        """Загружает все анимации из папок assets/character_name/"""
        base_path = os.path.join('assets', self.character_name)
        
        if not os.path.exists(base_path):
            raise FileNotFoundError(f"Папка с анимациями не найдена: {base_path}")
        
        # Сканируем папки с анимациями
        for animation_type in os.listdir(base_path):
            anim_path = os.path.join(base_path, animation_type)
            if os.path.isdir(anim_path):
                self.load_animation_frames(animation_type, anim_path)
    
    def load_animation_frames(self, animation_type, folder_path):
        """Загружает кадры анимации из указанной папки"""
        frames = []
        
        # Получаем все файлы изображений из папки
        image_files = sorted([f for f in os.listdir(folder_path) 
                           if f.endswith(('.png', '.jpg', '.bmp'))])
        
        for img_file in image_files:
            try:
                img_path = os.path.join(folder_path, img_file)
                frame = pygame.image.load(img_path).convert_alpha()
                frame = pygame.transform.scale(frame, self.size)
                frames.append((frame, ANIMATION_DELAY))
            except Exception as e:
                print(f"Ошибка загрузки кадра {img_file}: {e}")
        
        if frames:
            anim = pyganim.PygAnimation(frames)
            anim.play()
            self.animations[animation_type] = anim
    
    def update_animation(self, state):
        """
        Обновляет текущую анимацию на основе состояния персонажа
        :param state: словарь с состояниями, например:
            {
                'moving_left': True,
                'moving_right': False,
                'jumping': True,
                'on_ground': False,
                'attacking': False
            }
        """
        self.image.fill((0, 0, 0, 0))  # Очищаем с прозрачным фоном
        
        # Определяем какая анимация должна проигрываться
        animation_type = 'idle'  # По умолчанию
        
        if state.get('attacking', False):
            animation_type = 'attack'
        elif state.get('jumping', False):
            if not state.get('on_ground', True):
                if state.get('moving_left', False):
                    animation_type = 'jump_left'
                elif state.get('moving_right', False):
                    animation_type = 'jump_right'
                else:
                    animation_type = 'jump'
        elif state.get('moving_left', False):
            animation_type = 'run'
            self.facing_left = True
        elif state.get('moving_right', False):
            animation_type = 'run'
            self.facing_left = False
        
        # Получаем нужную анимацию
        anim = self.animations.get(animation_type)
        if anim is None:
            # Если анимация не найдена, пробуем найти похожую
            anim = self.animations.get('idle')
        
        # Проигрываем анимацию
        if anim:
            anim.blit(self.image, (0, 0))
        
        # Отражаем изображение если нужно
        if self.facing_left:
            self.image = pygame.transform.flip(self.image, True, False)
    
    def get_image(self):
        """Возвращает текущее изображение с анимацией"""
        return self.image