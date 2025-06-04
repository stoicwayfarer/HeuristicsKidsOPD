SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 750

PLAYER_SPEED = 10
enemy_positions = [
        (300, 420),  
        (350, 270),
        (700, 420)
    ]

BACKGROUND_COLOR = (207, 229, 250)
PLAYER_COLOR = (120, 94, 130)
GRAVITY = 0.8
FRICTION = -.12
JUMP_STRENGTH = -15
MAX_FALL_SPEED = 15
START_POSITION_LVL_1 = (200,620)
###Цвета###
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GROUND_COLOR = (139, 69, 19)

# Размеры мира
WORLD_WIDTH = 5000  # Длинное игровое поле для платформера
WORLD_HEIGHT = SCREEN_HEIGHT *3
GROUND_HEIGHT = 150  # Высота "земли" от нижнего края экрана

### Константы камеры ###
CAMERA_WIDTH = SCREEN_WIDTH
CAMERA_HEIGHT = SCREEN_HEIGHT
CAMERA_BORDER_LEFT = 0.3  # Границы камеры (30% от ширины)
CAMERA_BORDER_RIGHT = 0.7
CAMERA_BORDER_TOP = 0.5
CAMERA_BORDER_BOTTOM = 0.7

CAMERA_BORDER_COLOR = (255, 0, 0)
CAMERA_BORDER_ALPHA = 128
CAMERA_BORDER_WIDTH = 2