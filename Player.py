import pygame
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
PLAYER_SPEED = 10

BACKGROUND_COLOR = (207, 229, 250)
PLAYER_COLOR = (120, 94, 130)
GRAVITY = 0.8
JUMP_STRENGTH = -15
MAX_FALL_SPEED = 15  

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
TEST_LEVEL=10000


### Константы камеры ###
CAMERA_WIDTH = SCREEN_WIDTH   # Ширина области камеры (обычно равна ширине экрана)
CAMERA_HEIGHT = SCREEN_HEIGHT    # Высота области камеры (обычно равна высоте экрана)

# Границы свободного движения внутри камеры (в долях от размера камеры)
# Когда игрок пересекает эти границы, камера начинает двигаться
CAMERA_BORDER_LEFT = 0.3    # 30% от левого края
CAMERA_BORDER_RIGHT = 0.7   # 70% от левого края (или 30% от правого)
CAMERA_BORDER_TOP = 0.3   # 30% от верхнего края
CAMERA_BORDER_BOTTOM = 0.7  # 70% от верхнего края (или 30% от нижнего)

# Цвет и прозрачность границ камеры (для визуализации)
CAMERA_BORDER_COLOR = (255, 0, 0)
CAMERA_BORDER_ALPHA = 128          # Полупрозрачный (0-255)
CAMERA_BORDER_WIDTH = 2            # Толщина линии границы

class Player(pygame.sprite.Sprite):
    global TEST_LEVEL
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((100, 100))
        self.image.fill(PLAYER_COLOR) 
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT 
        self.change_x = 0
        self.change_y = 0
        self.facing_right = True
        self.on_ground = True 

    def update(self):

        self.rect.x += self.change_x
        
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH+TEST_LEVEL:
            self.rect.right = SCREEN_WIDTH+TEST_LEVEL
            
        if not self.on_ground:
            self.change_y += GRAVITY
            if self.change_y > MAX_FALL_SPEED:
                self.change_y = MAX_FALL_SPEED
        
        self.rect.y += self.change_y
        

        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.change_y = 0
            self.on_ground = True
        else:
            self.on_ground = False
            

        if self.rect.top < 0:
            self.rect.top = 0
            self.change_y = 0  

    def go_left(self):
        self.change_x = -PLAYER_SPEED
        if self.facing_right:
            self.flip()
            self.facing_right = False 

    def go_right(self):
        self.change_x = PLAYER_SPEED
        if not self.facing_right: 
            self.flip()
            self.facing_right = True 

    def jump(self):
        if self.on_ground:
            self.change_y = JUMP_STRENGTH
            self.on_ground = False

    def stop(self):
        self.change_x = 0

    def flip(self):
        self.image = pygame.transform.flip(self.image, True, False)