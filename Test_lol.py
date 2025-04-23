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

WORLD_WIDTH = 10000  # Ширина игрового мира
GROUND_HEIGHT = 0 # Высота "земли" от нижнего края экрана
GROUND_COLOR = (139, 69, 19)  # Коричневый цвет для земли

### Константы камеры ###
CAMERA_WIDTH = SCREEN_WIDTH
CAMERA_HEIGHT = SCREEN_HEIGHT  # Камера теперь охватывает весь экран

# Границы свободного движения внутри камеры
CAMERA_BORDER_LEFT = 0.4
CAMERA_BORDER_RIGHT = 0.6
CAMERA_BORDER_TOP = 0.6
CAMERA_BORDER_BOTTOM = 0.7

# Цвет и прозрачность границ камеры
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
        self.rect.bottom = SCREEN_HEIGHT - GROUND_HEIGHT  # Позиционируем относительно земли
        self.change_x = 0
        self.change_y = 0
        self.facing_right = True
        self.on_ground = True

    def update(self):
        self.rect.x += self.change_x

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WORLD_WIDTH:
            self.rect.right = WORLD_WIDTH

        if not self.on_ground:
            self.change_y += GRAVITY
            if self.change_y > MAX_FALL_SPEED:
                self.change_y = MAX_FALL_SPEED

        self.rect.y += self.change_y

        # Проверка столкновения с землей с учетом GROUND_HEIGHT
        if self.rect.bottom >= SCREEN_HEIGHT - GROUND_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT - GROUND_HEIGHT
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


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("COFFEFU")

    # Создаем мир
    world_surface = pygame.Surface((WORLD_WIDTH, SCREEN_HEIGHT))
    world_surface.fill(BACKGROUND_COLOR)

    # Рисуем сетку на мире
    for x in range(0, WORLD_WIDTH, 100):
        pygame.draw.line(world_surface, (200, 200, 200), (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, 100):
        pygame.draw.line(world_surface, (200, 200, 200), (0, y), (WORLD_WIDTH, y))

    # Рисуем землю на мире (теперь она часть мирового Surface)
    ground_rect = pygame.Rect(0, SCREEN_HEIGHT - GROUND_HEIGHT, WORLD_WIDTH, GROUND_HEIGHT)
    pygame.draw.rect(world_surface, GROUND_COLOR, ground_rect)

    player = Player()
    all_sprites = pygame.sprite.Group(player)
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

        # Отрисовка
        screen.fill(BLACK)

        # Рисуем мир со смещением камеры (включая землю)
        screen.blit(world_surface, (-camera.offset_x, -camera.offset_y))

        # Рисуем спрайты с учетом смещения камеры
        for sprite in all_sprites:
            screen.blit(sprite.image, camera.apply(sprite.rect))

        # Визуализация границ камеры (опционально)
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