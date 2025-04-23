import pygame
from abc import ABC, abstractmethod

###Константы### 
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



###От Марины###
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

###Стартовое окно (Димка)###
def start_screen():
    global SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE
    pygame.init()
    start_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("COFFEFU")


    background = pygame.image.load("Image/Test.Fon.jpg").convert()  #Фон старт окна
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT)) 

    #Шрифты
    title_font = pygame.font.Font('Fonts/MochiyPopOne-Regular.ttf', 54)
    developers_font = pygame.font.SysFont('Comic Sans MS',54)
    button_font = pygame.font.SysFont('Comic Sans MS', 36)

    # Текст
    title_text = title_font.render("COFFEFU", True, BLACK)
    developers_text= developers_font.render("Heuristics kids", True, BLACK)
    start_text = button_font.render("Начать игру", True, BLACK)
    exit_text = button_font.render("Выйти", True, BLACK)

    # Прямоугольники для кнопок
    start_button = pygame.Rect(300, 250, 200, 50)
    exit_button = pygame.Rect(300, 350, 200, 50)

    running = True
    while running:
        start_screen.blit(background, (0, 0))

        # Отображение текста
        start_screen.blit(title_text, (800,135))
        start_screen.blit(developers_text,(200,900))

        # Отрисовка кнопок
        button_surface = pygame.Surface((200, 50), pygame.SRCALPHA)
        button_surface.fill(WHITE)
        start_screen.blit(button_surface, (300, 250))
        start_screen.blit(button_surface, (300, 350))

        # Текст на кнопках
        start_screen.blit(start_text, (300 + (200 - start_text.get_width()) // 2, 250 + (50 - start_text.get_height()) // 2))
        start_screen.blit(exit_text, (300 + (200 - exit_text.get_width()) // 2, 350 + (50 - exit_text.get_height()) // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_RETURN:
                    running = False
                    return True

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                if start_button.collidepoint(mouse_pos):
                    running = False
                    return True

                if exit_button.collidepoint(mouse_pos):
                    running = False
                    pygame.quit()
                    return False

    pygame.quit()
    return False
#############


###От Димы камера (Надо доработать жеско)###
class Camera:
    def __init__(self, width, height):
        self.camera_rect = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.offset_x = 0
        self.offset_y = 0

    def apply(self, rect):

        return rect.move(-self.offset_x, -self.offset_y)

    def update(self, target):
        border_left = self.camera_rect.left + self.width * CAMERA_BORDER_LEFT
        border_right = self.camera_rect.right - self.width * (1 - CAMERA_BORDER_RIGHT)
        border_top = self.camera_rect.top + self.height * CAMERA_BORDER_TOP
        border_bottom = self.camera_rect.bottom - self.height * (1 - CAMERA_BORDER_BOTTOM)

        if target.rect.left < border_left:
            self.camera_rect.left = target.rect.left - self.width * CAMERA_BORDER_LEFT
        elif target.rect.right > border_right:
            self.camera_rect.right = target.rect.right + self.width * (1 - CAMERA_BORDER_RIGHT)

        if target.rect.top < border_top:
            self.camera_rect.top = target.rect.top - self.height * CAMERA_BORDER_TOP
        elif target.rect.bottom > border_bottom:
            self.camera_rect.bottom = target.rect.bottom + self.height * (1 - CAMERA_BORDER_BOTTOM)

        self.offset_x = self.camera_rect.x
        self.offset_y = self.camera_rect.y


#####################################


def main():
    if not start_screen():
        return

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("COFFEFU")

    # Создаем мир большего размера
    world_width = SCREEN_WIDTH + TEST_LEVEL
    world_height = SCREEN_HEIGHT
    world_surface = pygame.Surface((world_width, world_height))
    world_surface.fill(BACKGROUND_COLOR)

    # Рисуем сетку
    for x in range(0, world_width, 100):
        pygame.draw.line(world_surface, (200, 200, 200), (x, 0), (x, world_height))
    for y in range(0, world_height, 100):
        pygame.draw.line(world_surface, (200, 200, 200), (0, y), (world_width, y))

    player = Player()
    all_sprites = pygame.sprite.Group(player)

    # Создаем камеру с размерами экрана
    camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

    # Начальная позиция камеры (центрируем на игроке)
    camera.camera_rect.center = player.rect.center

    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_a:
                    player.go_left()
                elif event.key == pygame.K_d:
                    player.go_right()
                if event.key == pygame.K_SPACE or event.key == pygame.K_w:
                    player.jump()
                elif event.key == pygame.K_ESCAPE: 
                    running = False
            elif event.type == pygame.KEYUP: 
                if event.key == pygame.K_a and player.change_x < 0:
                    player.stop()
                elif event.key == pygame.K_d and player.change_x > 0:
                    player.stop()

        all_sprites.update()
        camera.update(player)

        # Отрисовка
        screen.fill(BLACK)

        # Рисуем мир со смещением камеры
        screen.blit(world_surface, (-camera.offset_x, -camera.offset_y))

        # Рисуем спрайты с учетом смещения камеры
        for sprite in all_sprites:
            screen.blit(sprite.image, camera.apply(sprite.rect))

        # Рисуем границы камеры (для наглядности)
        pygame.draw.rect(screen, (255, 0, 0), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 3)

        # Прозрачная поверхность для рамки
        border_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

        # Верхняя граница
        pygame.draw.rect(border_surface, (*CAMERA_BORDER_COLOR, CAMERA_BORDER_ALPHA),
                 (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT * CAMERA_BORDER_TOP), 
                 CAMERA_BORDER_WIDTH)
        pygame.draw.rect(border_surface, (*CAMERA_BORDER_COLOR, CAMERA_BORDER_ALPHA),
                 (0, SCREEN_HEIGHT * CAMERA_BORDER_BOTTOM, 
                  SCREEN_WIDTH, SCREEN_HEIGHT * (1 - CAMERA_BORDER_BOTTOM)), 
                 CAMERA_BORDER_WIDTH)
        pygame.draw.rect(border_surface, (*CAMERA_BORDER_COLOR, CAMERA_BORDER_ALPHA),
                 (0, 0, SCREEN_WIDTH * CAMERA_BORDER_LEFT, SCREEN_HEIGHT), 
                 CAMERA_BORDER_WIDTH)
        pygame.draw.rect(border_surface, (*CAMERA_BORDER_COLOR, CAMERA_BORDER_ALPHA),
                 (SCREEN_WIDTH * CAMERA_BORDER_RIGHT, 0, 
                  SCREEN_WIDTH * (1 - CAMERA_BORDER_RIGHT), SCREEN_HEIGHT), 
                 CAMERA_BORDER_WIDTH)

        screen.blit(border_surface, (0, 0))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()