import pygame
from config import *

class BaseScreen:
    def __init__(self, width, height):
        self.SCREEN_WIDTH = width
        self.SCREEN_HEIGHT = height
        self.BLACK = BLACK
        self.WHITE = WHITE
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.background = None
        self.running = False

    def create_button(self, surface, text, font, x, y, width, height, text_color, button_color):
        button_rect = pygame.Rect(x, y, width, height)
        button_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        button_surface.fill(button_color)
        surface.blit(button_surface, (x, y))
        
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=button_rect.center)
        surface.blit(text_surface, text_rect)
        
        return button_rect

    def load_background(self, image_path):
        self.background = pygame.image.load(image_path).convert()
        self.background = pygame.transform.scale(self.background, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

    def run(self):
        self.running = True
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
        
        
        return self.get_result()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.on_quit()
            self.process_event(event)

    def process_event(self, event):
        pass

    def update(self):
        pass

    def draw(self):
        if self.background:
            self.screen.blit(self.background, (0, 0))

    def on_quit(self):
        pass

    def get_result(self):
        return False


class Button:
    def __init__(self, x, y, width, height, text, font, 
                 normal_color, hover_color, text_color, 
                 border_radius=0, border_width=0, border_color=None,
                 audio_manager=None, sound_name=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.normal_color = normal_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.current_color = normal_color
        self.border_radius = border_radius
        self.border_width = border_width
        self.border_color = border_color
        self.is_hovered = False
        self.was_hovered = False
        self.scale = 1.0
        self.target_scale = 1.0
        self.animation_speed = 0.1
        self.audio_manager = audio_manager
        self.sound_name = sound_name
        self.sound_played = False
        
    def update(self, mouse_pos):
        self.was_hovered = self.is_hovered
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
        # воспроизведение звука при наведении
        if self.is_hovered and not self.was_hovered and self.audio_manager and self.sound_name:
            self.audio_manager.play(self.sound_name)
            self.sound_played = True
        elif not self.is_hovered:
            self.sound_played = False
            
        if self.is_hovered != self.was_hovered:
            self.target_scale = 1.05 if self.is_hovered else 1.0
            
        if abs(self.scale - self.target_scale) > 0.01:
            self.scale += (self.target_scale - self.scale) * self.animation_speed
        else:
            self.scale = self.target_scale
            
        self.current_color = self.hover_color if self.is_hovered else self.normal_color
        
    def play_click_sound(self):
        if self.audio_manager and self.sound_name:
            self.audio_manager.play(self.sound_name)

    def draw(self, surface):
        scaled_width = int(self.rect.width * self.scale)
        scaled_height = int(self.rect.height * self.scale)
        scaled_x = self.rect.centerx - scaled_width // 2
        scaled_y = self.rect.centery - scaled_height // 2
        
        button_surface = pygame.Surface((scaled_width, scaled_height), pygame.SRCALPHA)
        
        if self.border_radius > 0:
            pygame.draw.rect(button_surface, self.current_color, 
                            button_surface.get_rect(), 
                            border_radius=self.border_radius)
            if self.border_width > 0 and self.border_color:
                pygame.draw.rect(button_surface, self.border_color, 
                                button_surface.get_rect(), 
                                self.border_width, 
                                self.border_radius)
        else:
            button_surface.fill(self.current_color)
        
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=(scaled_width//2, scaled_height//2))
        button_surface.blit(text_surface, text_rect)

        surface.blit(button_surface, (scaled_x, scaled_y))
        
        return self.rect


class StartScreen(BaseScreen):
    def __init__(self, width, height, audio_manager):
        super().__init__(width, height)
        pygame.display.set_caption("COFFEFU")
        self.load_background("Images&Sprites/Test222.jpeg")
        self.result = False
        self.audio_manager = audio_manager
        
        # Загружаем звук для кнопок, если он еще не загружен
        if 'button' not in self.audio_manager.sounds:
            self.audio_manager.load_sound('button', 'Sounds/Button_sound.wav')
        
        self.title_font = pygame.font.Font('Fonts/MochiyPopOne-Regular.ttf', 54)
        self.developers_font = pygame.font.SysFont('Comic Sans MS', 54)
        self.button_font = pygame.font.SysFont('Comic Sans MS', 36)

        self.title_text = self.title_font.render("COFFEFU", True, self.BLACK)
        self.developers_text = self.developers_font.render("Heuristics kids", True, self.BLACK)

        button_normal = (240, 240, 240, 200)
        button_hover = (255, 255, 255, 255)
        button_text = (50, 50, 50)
        
        self.start_button = Button(
            550, 300, 400, 60, "Начать игру", self.button_font,
            button_normal, button_hover, button_text,
            border_radius=10, border_width=2, border_color=(200, 200, 200),
            audio_manager=self.audio_manager, sound_name='button'
        )
        
        self.exit_button = Button(
            550, 400, 400, 60, "Выйти", self.button_font,
            button_normal, button_hover, button_text,
            border_radius=10, border_width=2, border_color=(200, 200, 200),
            audio_manager=self.audio_manager, sound_name='button'
        )


    def update(self):
        super().update()
        mouse_pos = pygame.mouse.get_pos()
        
        self.start_button.update(mouse_pos)
        self.exit_button.update(mouse_pos)
        

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.background, (self.SCREEN_WIDTH, 0))
        
        
        #заголовок с тенью
        shadow_offset = 3
        title_shadow = self.title_font.render("COFFEFU", True, (0, 0, 0, 150))
        self.screen.blit(title_shadow, (590 + shadow_offset, 100 + shadow_offset))
        self.screen.blit(self.title_text, (590, 100))
        
        self.screen.blit(self.developers_text, (20, 680))
        
        start_rect = self.start_button.draw(self.screen)
        exit_rect = self.exit_button.draw(self.screen)
        
        self.start_button.rect = start_rect
        self.exit_button.rect = exit_rect

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False
            if event.key == pygame.K_RETURN:
                self.result = True
                self.running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

            if self.start_button.rect.collidepoint(mouse_pos):
                self.start_button.play_click_sound()
                self.result = True
                self.running = False

            if self.exit_button.rect.collidepoint(mouse_pos):
                self.exit_button.play_click_sound()
                self.running = False

    def get_result(self):
        return self.result

class DeadScreen(BaseScreen):
    def __init__(self, width, height, audio_manager):
        super().__init__(width, height)
        
        self.load_background("Images&Sprites/dead_screen.png")
        self.result = False
        self.audio_manager = audio_manager
        
        if 'button' not in self.audio_manager.sounds:
            self.audio_manager.load_sound('button', 'Sounds/Button_sound.wav')
        
        self.title_font = pygame.font.SysFont('Comic Sans MS', 54)
        self.button_font = pygame.font.SysFont('Comic Sans MS', 36)

        self.title_text = self.title_font.render("Вы проиграли :(", True, self.WHITE)


        button_normal = (200, 50, 50, 200)    # темно-красный
        button_hover = (255, 80, 80, 255)     # ярко-красный
        button_text = (255, 255, 255)         # белый текст
        
        # Создаем кнопки с анимацией и звуком
        self.restart_button = Button(
            550, 300, 400, 60, "Начать сначала", self.button_font,
            button_normal, button_hover, button_text,
            border_radius=10, border_width=2, border_color=(150, 40, 40),
            audio_manager=self.audio_manager, sound_name='button'
        )
        
        self.exit_button = Button(
            550, 400, 400, 60, "Выйти", self.button_font,
            button_normal, button_hover, button_text,
            border_radius=10, border_width=2, border_color=(150, 40, 40),
            audio_manager=self.audio_manager, sound_name='button'
        )

    def update(self):
        super().update()
        mouse_pos = pygame.mouse.get_pos()
        
        self.restart_button.update(mouse_pos)
        self.exit_button.update(mouse_pos)

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        
        #заголовок с тенью
        shadow_offset = 3
        title_shadow = self.title_font.render("Вы проиграли", True, (0, 0, 0, 150))
        self.screen.blit(title_shadow, (550 + shadow_offset, 100 + shadow_offset))
        self.screen.blit(self.title_text, (550, 100))
 
        restart_rect = self.restart_button.draw(self.screen)
        exit_rect = self.exit_button.draw(self.screen)
        
        self.restart_button.rect = restart_rect
        self.exit_button.rect = exit_rect

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False
            if event.key == pygame.K_RETURN:
                self.result = True
                self.running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

            if self.restart_button.rect.collidepoint(mouse_pos):
                self.restart_button.play_click_sound()
                self.result = True
                self.running = False

            if self.exit_button.rect.collidepoint(mouse_pos):
                self.exit_button.play_click_sound()
                self.running = False

    def get_result(self):
        return self.result
    
class LevelCompleteScreen(BaseScreen):
    def __init__(self, width, height, audio_manager, time_elapsed):
        super().__init__(width, height)
        
        self.load_background("Images&Sprites/NextLV.png")
        self.result = False
        self.time_elapsed = time_elapsed
        self.audio_manager = audio_manager
        self.sound_played = False
        
        if 'button' not in self.audio_manager.sounds:
            self.audio_manager.load_sound('button', 'Sounds/Button_sound.wav')
        if 'success' not in self.audio_manager.sounds:
            self.audio_manager.load_sound('success', 'Sounds/Success_sound.mp3')

        self.title_font =pygame.font.SysFont('Comic Sans MS', 54)
        self.time_font = pygame.font.SysFont('Comic Sans MS', 36)
        self.button_font = pygame.font.SysFont('Comic Sans MS', 36)

        self.title_text = self.title_font.render("Уровень пройден!", True, (50, 200, 50))
        self.time_text = self.time_font.render(f"Затраченное время: {self.format_time(time_elapsed)}", True, self.WHITE)

        button_normal = (100, 200, 100, 200)    # Зеленый
        button_hover = (150, 255, 150, 255)     # Светло-зеленый
        button_text = (255, 255, 255)           # Белый текст
        
        self.next_level_button = Button(
            550, 350, 400, 60, "Следующий уровень", self.button_font,
            button_normal, button_hover, button_text,
            border_radius=10, border_width=2, border_color=(50, 150, 50),
            audio_manager=self.audio_manager, sound_name='button'
        )
        
        self.exit_button = Button(
            550, 450, 400, 60, "Выйти", self.button_font,
            button_normal, button_hover, button_text,
            border_radius=10, border_width=2, border_color=(50, 150, 50),
            audio_manager=self.audio_manager, sound_name='button'
        )

    def run(self):
        if not self.sound_played and 'success' in self.audio_manager.sounds:
            self.audio_manager.play('success')
            self.sound_played = True
        return super().run()
    
    def format_time(self, seconds):
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02d}:{seconds:02d}"

    def update(self):
        super().update()
        mouse_pos = pygame.mouse.get_pos()

        self.next_level_button.update(mouse_pos)
        self.exit_button.update(mouse_pos)

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        
        #темный фон
        overlay = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 100))
        self.screen.blit(overlay, (0, 0))
        
        shadow_offset = 3
        title_shadow = self.title_font.render("Уровень пройден!", True, (0, 0, 0, 150))
        self.screen.blit(title_shadow, (520 + shadow_offset, 150 + shadow_offset))
        self.screen.blit(self.title_text, (520, 150))
        
        time_shadow = self.time_font.render(f"Затраченное время: {self.format_time(self.time_elapsed)}", True, (0, 0, 0, 150))
        self.screen.blit(time_shadow, (530 + shadow_offset, 220 + shadow_offset))
        self.screen.blit(self.time_text, (530, 220))
        
        next_rect = self.next_level_button.draw(self.screen)
        exit_rect = self.exit_button.draw(self.screen)
        
        self.next_level_button.rect = next_rect
        self.exit_button.rect = exit_rect

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False
            if event.key == pygame.K_RETURN:
                self.result = True
                self.running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

            if self.next_level_button.rect.collidepoint(mouse_pos):
                self.next_level_button.play_click_sound()
                self.result = True
                self.running = False

            if self.exit_button.rect.collidepoint(mouse_pos):
                self.exit_button.play_click_sound()
                self.running = False

    def get_result(self):
        return self.result
    
class FinalScreen(BaseScreen):
    def __init__(self, width, height, audio_manager):
        super().__init__(width, height)
        self.load_background("Images&Sprites/NextLV.png")
        self.result = None
        self.audio_manager = audio_manager
        self.sound_played = False
        
        # Загружаем звуки
        if 'button' not in self.audio_manager.sounds:
            self.audio_manager.load_sound('button', 'Sounds/Button_sound.wav')
        if 'final' not in self.audio_manager.sounds:
            self.audio_manager.load_sound('final', 'Sounds/Win_sound.mp3')
        
        # Шрифты
        self.title_font = pygame.font.SysFont('Comic Sans MS', 54)
        self.devs_font = pygame.font.SysFont('Comic Sans MS', 36)
        self.button_font = pygame.font.SysFont('Comic Sans MS', 36)

        self.title_text = self.title_font.render("Спасибо за прохождение игры!", True, (50, 200, 50))
        self.devs_text = self.devs_font.render("Разработчики: Постникова Марина и Кретов Дмитрий", True, self.WHITE)

        button_normal = (200, 150, 0, 200)    # Золотой
        button_hover = (255, 200, 0, 255)     # Яркий золотой
        button_text = (255, 255, 255)         # Белый текст
        
        self.menu_button = Button(
            550, 350, 400, 60, "Главное меню", self.button_font,
            button_normal, button_hover, button_text,
            border_radius=10, border_width=2, border_color=(150, 100, 0),
            audio_manager=self.audio_manager, sound_name='button'
        )
        
        self.exit_button = Button(
            550, 450, 400, 60, "Выйти", self.button_font,
            button_normal, button_hover, button_text,
            border_radius=10, border_width=2, border_color=(150, 100, 0),
            audio_manager=self.audio_manager, sound_name='button'
        )

    def run(self):
        if not self.sound_played and 'final' in self.audio_manager.sounds:
            self.audio_manager.play('final')
            self.sound_played = True
        return super().run()

    def update(self):
        super().update()
        mouse_pos = pygame.mouse.get_pos()
        self.menu_button.update(mouse_pos)
        self.exit_button.update(mouse_pos)

    def draw(self):
        self.screen.blit(self.background, (0, 0))

        overlay = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 100))
        self.screen.blit(overlay, (0, 0))
        
        shadow_offset = 3
        title_shadow = self.title_font.render("Спасибо за прохождение игры!", True, (0, 0, 0, 150))
        title_x = (self.SCREEN_WIDTH - self.title_text.get_width()) // 2
        self.screen.blit(title_shadow, (title_x + shadow_offset, 150 + shadow_offset))
        self.screen.blit(self.title_text, (title_x, 150))
        
        devs_shadow = self.devs_font.render("Разработчики: Постникова Марина и Кретов Дмитрий", True, (0, 0, 0, 150))
        devs_x = (self.SCREEN_WIDTH - self.devs_text.get_width()) // 2
        self.screen.blit(devs_shadow, (devs_x + shadow_offset, 220 + shadow_offset))
        self.screen.blit(self.devs_text, (devs_x, 220))
        
        menu_rect = self.menu_button.draw(self.screen)
        exit_rect = self.exit_button.draw(self.screen)
        
        self.menu_button.rect = menu_rect
        self.exit_button.rect = exit_rect

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False
                self.result = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

            if self.menu_button.rect.collidepoint(mouse_pos):
                self.menu_button.play_click_sound()
                self.result = "menu"
                self.running = False

            if self.exit_button.rect.collidepoint(mouse_pos):
                self.exit_button.play_click_sound()
                self.result = False
                self.running = False

    def get_result(self):
        return self.result