import pygame
import sys
from config import *
from tilemap import *
from animations import *
from spritesheet import Spritesheet
from player import Player, Enemy

class Level:
    def __init__(self, level_number, map_file, enemy_positions):
        self.level_number = level_number
        self.spritesheet = Spritesheet('spritesheet.png')
        self.map = TileMap(map_file, self.spritesheet)

        # Create enemy group
        self.enemies = pygame.sprite.Group()
        for pos in enemy_positions:
            enemy = Enemy(*pos)
            self.enemies.add(enemy)
            
        # Create player and set starting position
        self.player = Player(self.enemies)
        self.player.position.x, self.player.position.y = START_POSITION_LVL_1

        self.score = 0
        # Timer
        self.timer = 60  # Set timer to 60 seconds
        self.font = pygame.font.Font(None, 36)
        self.start_time = pygame.time.get_ticks()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.player.LEFT_KEY = True
                elif event.key == pygame.K_d:
                    self.player.RIGHT_KEY = True
                elif event.key == pygame.K_SPACE:
                    self.player.jump()
                elif event.key == pygame.K_f: 
                    self.player.attack()
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.player.LEFT_KEY = False
                elif event.key == pygame.K_d:
                    self.player.RIGHT_KEY = False
                elif event.key == pygame.K_SPACE:
                    if self.player.is_jumping:
                        self.player.velocity.y *= .25
                        self.player.is_jumping = False

    def update(self, dt):
    # Обновляем игрока и врагов
        self.player.update(dt, self.map.tiles, self.enemies)
        for enemy in self.enemies:
            enemy.update(dt, self.player, self.map.tiles)
        
        if self.player.hp <= 0:
            self.restart_game()
    
    # Обновляем таймер
        elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000
        self.timer = max(0, 60 - int(elapsed_time))
    
        current_killed_count = len(self.player.killed_enemies)
        self.score = current_killed_count * 100  
    
    # Проверка на переход на новый уровень
        if self.score >= 500:
            self.next_level()

        if self.timer == 0:
            self.restart_level()

    def next_level(self):
    # Переход на следующий уровень
        if self.level_number + 1 < len(levels_data):
            self.level_number += 1
            self.__init__(self.level_number, levels_data[self.level_number]['map'], levels_data[self.level_number]['enemies'])
        else:
            print("Вы прошли все уровни!")
            pygame.quit()
            sys.exit()

    def draw(self, screen):
        screen.fill(BACKGROUND_COLOR)
        self.map.draw_map(screen)
        
        for enemy in self.enemies:
            enemy.draw(screen)
            
        self.player.draw(screen)
        
        # Draw timer
        timer_text = self.font.render(f'Time: {self.timer}', True, (255, 255, 255))
        screen.blit(timer_text, (10, 10))
        hp_text = self.font.render(f'HP: {self.player.hp}', True, (255, 255, 255))
        screen.blit(hp_text, (10, 40))
        score_text = self.font.render(f'SCORE: {self.score}', True, (255, 255, 255))
        screen.blit(score_text, (1200, 10))
        level_text = self.font.render(f'LEVEL: {self.level_number + 1}', True, (255, 255, 255))
        screen.blit(level_text, (750, 10))

    def restart_level(self):
        self.player.position.x, self.player.position.y = START_POSITION_LVL_1
        self.player.velocity = pygame.math.Vector2(0, 0)
        self.player.hp = self.player.max_hp
        for enemy in self.enemies:
            enemy.respawn()

        self.player.killed_enemies = []
            
        self.start_time = pygame.time.get_ticks()
        self.timer = 60  # Reset timer to 60 seconds

    def restart_game(self):
        # Сбросить игру на первый уровень
        self.level_number = 0
        self.__init__(self.level_number, levels_data[self.level_number]['map'], levels_data[self.level_number]['enemies'])

def main():
    pygame.init()
    screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Game Levels")
    clock = pygame.time.Clock()

    global levels_data
    # Enemy positions for each level
    levels_data = [
        {
            'map': 'level_1.csv',
            'enemies': [(300, 420), (350, 270), (700, 420)]
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

    # Create levels
    levels = [Level(i, data['map'], data['enemies']) for i, data in enumerate(levels_data)]
    current_level = levels[0]

    running = True
    while running:
        dt = clock.tick(60) * 0.001 * 60  # Calculate dt
        
        current_level.handle_events()
        current_level.update(dt)
        
        # Draw
        current_level.draw(screen)
        window.blit(screen, (0, 0))
        pygame.display.update()

if __name__ == "__main__":
    main()
      