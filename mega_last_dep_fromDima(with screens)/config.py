#Размеры экрана и мира
SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 750

WORLD_WIDTH = 3000
WORLD_HEIGHT = 750

PLAYER_SPEED = 10
enemy_positions = [
        (640, 544),  
        (832, 480),
        (1104, 416),
        (1328, 368),
        (1184, 272),
        (1408, 192),
        (1680, 128),
        (2240, 192),
        (2512, 240),
        (2800, 320),
        (2608,528)
    ]

ANIMATION_DELAY = 200

BACKGROUND_COLOR = (232, 217, 252)
PLAYER_COLOR = (120, 94, 130)
GRAVITY = 0.8
FRICTION = -.12
JUMP_STRENGTH = -15
MAX_FALL_SPEED = 15
START_POSITION_LVL_1 = (200, 544)

###Цвета###
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GROUND_COLOR = (139, 69, 19)

#Звуки и музыка
SOUNDS_PATHS = {
    'run': 'Sounds/CoolRun.wav',
    'jump': 'Sounds/Jump.mp3',
    'hit': 'Sounds/Hit.wav',
    'button': 'Sounds/Button_sound.wav',
    'background1':'Sounds/Background1.mp3',
    'background2':'Sounds/Background2.mp3',
    'Death_player':'Sounds/Death_player_sound.mp3',
    'exit_sound':'Sounds/Exit_sound.mp3',
    'Game_over':'Sounds/Game_over.mp3',
    'success':'Sounds/Success_sound.mp3',
    'Win':'Sounds/Win_sound.mp3',

}