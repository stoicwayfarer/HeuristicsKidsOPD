import pygame
import random
### Константы ###
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
PLAYER_SPEED = 10

BACKGROUND_COLOR = (207, 229, 250)
PLAYER_COLOR = (120, 94, 130)
GRAVITY = 0.8
JUMP_STRENGTH = -15
MAX_FALL_SPEED = 15

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

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((100, 100))
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = WORLD_HEIGHT - GROUND_HEIGHT  # Позиционируем относительно земли
        self.change_x = 0
        self.change_y = 0
        self.facing_right = True
        self.on_ground = True

    def update(self):
        self.rect.x += self.change_x

        # Границы по X +тут под кубик
        if self.rect.left < 155:
            self.rect.left = 155
        if self.rect.right > WORLD_WIDTH-155:
            self.rect.right = WORLD_WIDTH-155

        if not self.on_ground:
            self.change_y += GRAVITY
            if self.change_y > MAX_FALL_SPEED:
                self.change_y = MAX_FALL_SPEED

        self.rect.y += self.change_y

        # Cтолкновения с землей
        if self.rect.bottom >= WORLD_HEIGHT - GROUND_HEIGHT:
            self.rect.bottom = WORLD_HEIGHT - GROUND_HEIGHT
            self.change_y = 0
            self.on_ground = True
        else:
            self.on_ground = False

        # Границы по Y
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

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, patrol_range=300, speed=3):
        super().__init__()
        self.image = pygame.Surface((80, 80))
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = y
        self.patrol_range = patrol_range  # Диапазон патрулирования
        self.speed = speed
        self.direction = -1  # 1 - вправо, -1 - влево
        self.start_x = x  # Начальная позиция для патрулирования
        
    def update(self):
        # Движение влево-вправо
        self.rect.x += self.speed * self.direction
        
        # Проверка границ патрулирования
        if self.rect.x > self.start_x + self.patrol_range:
            self.direction = -1
        elif self.rect.x < self.start_x:
            self.direction = 1
            
        # Ограничение по границам мира
        if self.rect.left < 0:
            self.rect.left = 0
            self.direction = 1
        if self.rect.right > WORLD_WIDTH:
            self.rect.right = WORLD_WIDTH
            self.direction = -1
       

	
def generate_enemies(count=5):
	enemies = pygame.sprite.Group()

	for _ in range(count):
		# Случайные параметры для врага
		x = random.randint(200, WORLD_WIDTH - 200)  # Не слишком близко к краям
		patrol_range = random.randint(200, 600)  # Разный диапазон патрулирования
		speed = random.uniform(2, 6)  # Разная скорость
		
		# Создаем врага на уровне земли
		enemy = Enemy(x, WORLD_HEIGHT - GROUND_HEIGHT, patrol_range, speed)
		
		# Проверяем, чтобы враги не пересекались друг с другом
		while any(e.rect.colliderect(enemy.rect) for e in enemies):
			x = random.randint(200, WORLD_WIDTH - 200)
			enemy.rect.x = x
		
		enemies.add(enemy)

	return enemies      
        

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

###Стартовое окно###
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
    start_button = pygame.Rect(850, 500, 200, 50) #dnclesdkn l
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
        start_screen.blit(button_surface, (850, 500))#ubcue
        start_screen.blit(button_surface, (300, 350))

        # Текст на кнопках
        start_screen.blit(start_text, (850 + (200 - start_text.get_width()) // 2, 500 + (50 - start_text.get_height()) // 2))
        start_screen.blit(exit_text, (850 + (200 - exit_text.get_width()) // 2, 699 + (50 - exit_text.get_height()) // 2))

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

def main():
    if not start_screen():
        return
    
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("COFFEFU")

    # Игровое поле 
    world_surface = pygame.Surface((WORLD_WIDTH, WORLD_HEIGHT))
    world_surface.fill(BACKGROUND_COLOR)

    # Сетка
    for x in range(0, WORLD_WIDTH, 100):
        pygame.draw.line(world_surface, (200, 200, 200), (x, 0), (x, WORLD_HEIGHT))
    for y in range(0, WORLD_HEIGHT, 100):
        pygame.draw.line(world_surface, (200, 200, 200), (0, y), (WORLD_WIDTH, y))

    # "Земля"
    ground_rect = pygame.Rect(0, WORLD_HEIGHT - GROUND_HEIGHT, WORLD_WIDTH, GROUND_HEIGHT)
    pygame.draw.rect(world_surface, GROUND_COLOR, ground_rect)

    player = Player()
    enemies = generate_enemies(10)
    all_sprites = pygame.sprite.Group(player,enemies)
	
    # enemy1 = Enemy(500, WORLD_HEIGHT - GROUND_HEIGHT , 1000, 10)
    # enemy2 = Enemy(1500, WORLD_HEIGHT - GROUND_HEIGHT, 200, 4)
    # enemy3 = Enemy(3000, WORLD_HEIGHT - GROUND_HEIGHT, 600, 7)

    # all_sprites = pygame.sprite.Group(player,enemy1, enemy2, enemy3)
    camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

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

        screen.fill(BLACK)

        # Видимая часть мира 
        screen.blit(world_surface, (-camera.offset_x, -camera.offset_y))

        # Рисуем спрайты с учетом смещения камеры
        for sprite in all_sprites:
            screen.blit(sprite.image, camera.apply(sprite.rect))

            # Границы камеры
        border_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
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
