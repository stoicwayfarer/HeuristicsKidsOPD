import pygame
from config import *

class BaseScreen:
    def __init__(self, width, height):
        self.SCREEN_WIDTH = width
        self.SCREEN_HEIGHT = height
        self.BLACK = BLACK
        self.WHITE = WHITE
        self.screen = pygame.display.set_mode((width, height))
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
        self.load_background("Images&Sprites/Test222.jpeg")
        self.result = False
        self.audio_manager = audio_manager
        
        self.title_font = pygame.font.Font('Fonts/MochiyPopOne-Regular.ttf', 54)
        self.developers_font = pygame.font.SysFont('Comic Sans MS', 54)
        self.button_font = pygame.font.SysFont('Comic Sans MS', 36)

        self.title_text = self.title_font.render("Candy Runner", True, self.BLACK)
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
        title_shadow = self.title_font.render("Candy Runner", True, (0, 0, 0, 150))
        self.screen.blit(title_shadow, (590 + shadow_offset, 100 + shadow_offset))
        self.screen.blit(self.title_text, (590, 100))
        
        self.screen.blit(self.developers_text, (20, 680))
        
        start_rect = self.start_button.draw(self.screen)
        exit_rect = self.exit_button.draw(self.screen)
        
        self.start_button.rect = start_rect
        self.exit_button.rect = exit_rect

    def process_event(self, event):
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
 
def draw_dead_screen(screen, score, restart_button, menu_button):
    #затемнение
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))

    title_font = pygame.font.SysFont('Comic Sans MS', 54)
    score_font = pygame.font.SysFont('Comic Sans MS', 36)
    
    title_text = title_font.render("Вы проиграли!", True, (200, 50, 50))
    score_text = score_font.render(f"Ваш счет: {score}", True, (255, 255, 255))

    shadow_offset = 3
    title_shadow = title_font.render("Вы проиграли!", True, (0, 0, 0, 150))
    score_shadow = score_font.render(f"Ваш счет: {score}", True, (0, 0, 0, 150))
    
    screen.blit(title_shadow, (555 + shadow_offset, 150 + shadow_offset))
    screen.blit(title_text, (555, 150))
    
    screen.blit(score_shadow, (633 + shadow_offset, 250 + shadow_offset))
    screen.blit(score_text, (633, 250))
    
    #рисуем кнопки
    mouse_pos = pygame.mouse.get_pos()
    restart_button.update(mouse_pos)
    menu_button.update(mouse_pos)
    restart_button.draw(screen)
    menu_button.draw(screen)

def draw_level_complete_screen(screen, next_level_button, menu_button, time_elapsed, level_number):

    minutes = int(time_elapsed // 60) #переводим время
    time_elapsed = int(time_elapsed % 60)

    #затемнение
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))
    
    title_font = pygame.font.SysFont('Comic Sans MS', 54)
    time_font = pygame.font.SysFont('Comic Sans MS', 36)
    
    title_text = title_font.render(f"Уровень {level_number} пройден!", True, (50, 200, 50))
    time_text = time_font.render(f"Затраченное время: {(f"{minutes:02d}:{time_elapsed:02d}")}", True, (255, 255, 255))

    shadow_offset = 3
    title_shadow = title_font.render(f"Уровень {level_number} пройден!", True, (0, 0, 0, 150))
    time_shadow = time_font.render(f"Затраченное время: {(f"{minutes:02d}:{time_elapsed:02d}")}", True, (0, 0, 0, 150))
    
    screen.blit(title_shadow, (510 + shadow_offset, 150 + shadow_offset))
    screen.blit(title_text, (510, 150))
    
    screen.blit(time_shadow, (530 + shadow_offset, 220 + shadow_offset))
    screen.blit(time_text, (530, 220))
    
    #рисуем кнопки
    mouse_pos = pygame.mouse.get_pos()
    next_level_button.update(mouse_pos)
    menu_button.update(mouse_pos)
    next_level_button.draw(screen)
    menu_button.draw(screen)
    
class FinalScreen(BaseScreen):
    def __init__(self, width, height, audio_manager):
        super().__init__(width, height)
        self.load_background("Images&Sprites/NextLV.png")
        self.result = None
        self.audio_manager = audio_manager
        self.sound_played = False
        
        #шрифты
        self.title_font = pygame.font.SysFont('Comic Sans MS', 54)
        self.devs_font = pygame.font.SysFont('Comic Sans MS', 36)
        self.button_font = pygame.font.SysFont('Comic Sans MS', 36)

        self.title_text = self.title_font.render("Спасибо за прохождение игры!", True, (50, 200, 50))
        self.devs_text = self.devs_font.render("Разработчики: Постникова Марина и Кретов Дмитрий", True, self.WHITE)

        button_normal = (200, 150, 0, 200) #золотой
        button_hover = (255, 200, 0, 255) #яркий золотой
        button_text = (255, 255, 255)
        
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