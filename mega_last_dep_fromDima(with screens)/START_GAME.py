import pygame
import sys
from config import *
from tilemap import *
from animations import *
from spritesheet import Spritesheet
from player import Player, Enemy
from Music import *
from Screens import *
from Camera import *

#pip install -r requirements.txt для установки пакетов из файла, необходимых для игры

class Level:
    def __init__(self, level_number, map_file, enemy_positions):
        self.level_number = level_number
        self.spritesheet = Spritesheet('spritesheet.png')
        self.map = TileMap(map_file, self.spritesheet)

        self.audio_manager = AudioManager()
        self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT, WORLD_WIDTH, WORLD_HEIGHT)
        
        self.enemies = pygame.sprite.Group()
        for pos in enemy_positions:
            enemy = Enemy(*pos)
            self.enemies.add(enemy)

        self.player = Player(self.enemies)
        self.player.position.x, self.player.position.y = START_POSITION_LVL_1

        #задаем параметры для уровня
        self.score = 0
        self.timer = 60
        self.points_to_next_level = 500

        self.font = pygame.font.Font(None, 36)
        self.start_time = pygame.time.get_ticks()
        self.level_complete = False
        self.level_complete_result = None
        self.game_over = False
        
        #стили для кнопок
        button_font = pygame.font.SysFont('Comic Sans MS', 36)
        
        level_button_normal = (100, 200, 100, 200)
        level_button_hover = (150, 255, 150, 255)
        level_button_text = (255, 255, 255)
        
        dead_button_normal = (200, 50, 50, 200)
        dead_button_hover = (255, 80, 80, 255)
        dead_button_text = (255, 255, 255)
        
        #кнопки для экрана перехода на уровень
        self.next_level_button = Button(
            550, 350, 400, 60, "Далее", button_font,
            level_button_normal, level_button_hover, level_button_text,
            border_radius=10, border_width=2, border_color=(50, 150, 50),
            audio_manager=self.audio_manager, sound_name='button'
        )
        
        self.menu_button = Button(
            550, 450, 400, 60, "Главное меню", button_font,
            level_button_normal, level_button_hover, level_button_text,
            border_radius=10, border_width=2, border_color=(50, 150, 50),
            audio_manager=self.audio_manager, sound_name='button'
        )
        
        #кнопки для экрана смерти
        self.restart_button = Button(
            550, 350, 400, 60, "Начать сначала", button_font,
            dead_button_normal, dead_button_hover, dead_button_text,
            border_radius=10, border_width=2, border_color=(150, 40, 40),
            audio_manager=self.audio_manager, sound_name='button'
        )
        
        self.exit_button = Button(
            550, 450, 400, 60, "Выйти", button_font,
            dead_button_normal, dead_button_hover, dead_button_text,
            border_radius=10, border_width=2, border_color=(150, 40, 40),
            audio_manager=self.audio_manager, sound_name='button'
        )

        self.audio_manager.play_music('background1') 

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if self.game_over:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if self.restart_button.rect.collidepoint(mouse_pos):
                        self.restart_button.play_click_sound()
                        self.restart_game()
                    elif self.exit_button.rect.collidepoint(mouse_pos):
                        self.exit_button.play_click_sound()
                        return "exit" 
                        
            elif not self.level_complete:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.player.LEFT_KEY = True
                    elif event.key == pygame.K_d:
                        self.player.RIGHT_KEY = True
                    elif event.key == pygame.K_SPACE:
                        self.player.jump()
                        self.audio_manager.play('jump')
                    elif event.key == pygame.K_f:
                        self.player.attack()
                        self.audio_manager.play('hit')

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.player.LEFT_KEY = False
                    elif event.key == pygame.K_d:
                        self.player.RIGHT_KEY = False
                    elif event.key == pygame.K_SPACE:
                        if self.player.is_jumping:
                            self.player.velocity.y *= .25
                            self.player.is_jumping = False
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if self.next_level_button.rect.collidepoint(mouse_pos):
                        self.next_level_button.play_click_sound()
                        self.level_complete_result = True
                    elif self.menu_button.rect.collidepoint(mouse_pos):
                        self.menu_button.play_click_sound()
                        self.level_complete_result = "menu"                
                       

        if not self.level_complete and not self.player.is_jumping and not self.game_over:
            if (self.player.LEFT_KEY or self.player.RIGHT_KEY):
                self.audio_manager.play_run()
            else:
                self.audio_manager.stop_run()
        else:
            self.audio_manager.stop_run()

        return None
    
    def update(self, dt):
        if self.game_over:
            return None
            
        if not self.level_complete:
            self.player.update(dt, self.map.tiles, self.enemies)
            for enemy in self.enemies:
                enemy.update(dt, self.player, self.map.tiles)

            if self.player.hp <= 0:
                self.game_over = True
                self.audio_manager.stop_music('background1')
                self.audio_manager.play('Death_plater')
                self.audio_manager.play('Game_over') 
                return None

            elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000
            self.timer = max(0, 60 - int(elapsed_time))

            current_killed_count = len(self.player.killed_enemies)
            self.score = current_killed_count * 100

            if self.score >= self.points_to_next_level and not self.level_complete:
                self.level_complete = True
                self.audio_manager.stop_music('background1')
                self.audio_manager.play('success')

            if self.timer == 0:
                self.game_over = True
                self.audio_manager.stop_music('background1')
                self.audio_manager.play('Death_plater')
                self.audio_manager.play('Game_over')
        
        if self.level_complete_result is not None:
            if self.level_complete_result == True:
                
                return self.next_level()
            elif self.level_complete_result == "menu":
                return "menu"
        
        return None

    def next_level(self):
        if self.level_number + 1 < len(levels_data):
            self.level_number += 1
            self.__init__(self.level_number, levels_data[self.level_number]['map'], levels_data[self.level_number]['enemies'])
        else:
            final_screen = FinalScreen(SCREEN_WIDTH, SCREEN_HEIGHT, self.audio_manager)
            self.audio_manager.play('Win')
            result = final_screen.run()
            return result
        return None

    def draw(self, screen):
        screen.fill(BACKGROUND_COLOR)
        self.camera.update(self.player)
        self.map.draw_map(screen, self.camera)

        for enemy in self.enemies:
            enemy.draw(screen, self.camera)

        self.player.draw(screen, self.camera)

        #вывод параметров(доработать, чтоб красиво)
        timer_text = self.font.render(f'Time: {self.timer}', True, (255, 255, 255))
        screen.blit(timer_text, (10, 10))
        hp_text = self.font.render(f'HP: {self.player.hp}', True, (255, 255, 255))
        screen.blit(hp_text, (10, 40))
        score_text = self.font.render(f'SCORE: {self.score}', True, (255, 255, 255))
        screen.blit(score_text, (1200, 10))
        level_text = self.font.render(f'LEVEL: {self.level_number + 1}', True, (255, 255, 255))
        screen.blit(level_text, (750, 10))

        if self.level_complete:
            draw_level_complete_screen(
                screen, 
                self.next_level_button, 
                self.menu_button, 
                (60 - self.timer),self.level_number+1
            )
        elif self.game_over:
            draw_dead_screen(
                screen,
                self.score,
                self.restart_button,
                self.exit_button
            )

    def restart_level(self):
        self.player.position.x, self.player.position.y = START_POSITION_LVL_1
        self.player.velocity = pygame.math.Vector2(0, 0)
        self.player.hp = self.player.max_hp
        for enemy in self.enemies:
            enemy.respawn()

        self.player.killed_enemies = []
        self.start_time = pygame.time.get_ticks()
        self.timer = 60
        self.level_complete = False
        self.level_complete_result = None

    def restart_game(self):
        self.audio_manager.stop_music('background1')
        self.level_number = 0
        self.__init__(self.level_number, levels_data[self.level_number]['map'], levels_data[self.level_number]['enemies'])

def main():
    pygame.init()

    while True:
        audio_manager = AudioManager()
        start_screen = StartScreen(SCREEN_WIDTH, SCREEN_HEIGHT, audio_manager)

        #запуск стартового экрана
        if not start_screen.run():
            pygame.quit()
            return

        screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Game Levels")
        clock = pygame.time.Clock()

        #задаем позиции врагов
        global levels_data
        levels_data = [
            {
                'map': 'level_1.csv',
                'enemies': enemy_positions
            },
            {
                'map': 'level_2.csv',
                'enemies': [(400, 300), (500, 200), (600, 400)]
            },
            {
                'map': 'level_3.csv',
                'enemies': [(200, 350), (450, 250), (700, 350)]
            }
        ]

        #делаем уровни
        levels = [Level(i, data['map'], data['enemies']) for i, data in enumerate(levels_data)]
        current_level = levels[0]

        running = True
        while running:
            dt = clock.tick(60) * 0.001 * 60
            
            result = current_level.handle_events()

            if result == "exit":
                current_level.audio_manager.stop_music('background1')
                pygame.quit()
                return
            
            update_result = current_level.update(dt)
            
            if update_result is not None:
                if update_result == "menu":
                    current_level.audio_manager.stop_music('background1')
                    break
                else:
                    current_level.audio_manager.stop_music('background1')
                    pygame.quit()
                    return
            
            #отрисовка
            current_level.draw(screen)
            window.blit(screen, (0, 0))
            pygame.display.update()

        continue

if __name__ == "__main__":
    main()
