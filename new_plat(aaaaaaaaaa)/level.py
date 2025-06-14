import pygame
from player import Player, Enemy
from tilemap import TileMap
from config import *

class Level:
    def __init__(self, level_num, spritesheet):
        self.level_num = level_num
        self.spritesheet = spritesheet
        self.reset_level()
        
    def reset_level(self):
        self.map_file = f'level_{self.level_num}.csv'
        self.time_limit = 120 * 1000
        self.start_time = pygame.time.get_ticks()
        self.enemy_value = 100
        self.score = 0
        self.load_level()
        
    def load_level(self):
        self.map = TileMap(self.map_file, self.spritesheet)
        self.enemies = pygame.sprite.Group()
        
        # Сохраняем начальные позиции врагов
        self._initial_enemy_positions = []  # Приватный атрибут
        
        if self.level_num == 1:
            positions = [(300, 420), (350, 270), (700, 420)]
        elif self.level_num == 2:
            positions = [(200, 400), (500, 300), (800, 400), (400, 200)]
        else:
            positions = [(150, 420), (300, 300), (600, 400), (750, 300), (900, 420)]
        
        self._initial_enemy_positions = positions.copy()
        for pos in positions:
            self.enemies.add(Enemy(*pos))
            
        self.player = Player(self.enemies)
        self.set_player_start_position()
    
    def respawn_all(self):
    # Респавн игрока
        self.player.position = pygame.math.Vector2(START_POSITION_LVL_1[0], START_POSITION_LVL_1[1])
        self.player.velocity = pygame.math.Vector2(0, 0)
        self.player.rect.x, self.player.rect.y = START_POSITION_LVL_1
        self.player.lives = 3
        self.player.killed_enemies = []
    
    # Полный респавн всех врагов
        for enemy in self.enemies:
            enemy.reset_state()  # Используем новый метод сброса
    
    # Сброс таймера и счета
        self.start_time = pygame.time.get_ticks()
        self.score = 0
    
    # Принудительная проверка коллизий для врагов
        for enemy in self.enemies:
            enemy.on_ground = False
            enemy.check_collisions_y(self.map.tiles)
    def set_player_start_position(self):
        start_x = 100
        start_y = 100
        if self.level_num == 1:
            start_y = 420 - self.player.rect.height
        elif self.level_num == 2:
            start_y = 300 - self.player.rect.height
        
        self.player.position.x, self.player.position.y = start_x, start_y
        self.player.rect.x, self.player.rect.y = start_x, start_y
        
    def update(self, dt):
        # Обновление игрока и врагов
        self.player.update(dt, self.map.tiles, self.enemies)
        
        for enemy in self.enemies:
            enemy.update(dt, self.player, self.map.tiles)
            
        # Обновление счета за убитых врагов
        if len(self.player.killed_enemies) > 0:
            self.score += self.enemy_value * len(self.player.killed_enemies)
            self.player.killed_enemies = []
            
        # Проверка завершения уровня (все враги мертвы)
        if all(not enemy.alive for enemy in self.enemies):
            return "level_complete"
            
        # Проверка истечения времени
        if pygame.time.get_ticks() - self.start_time > self.time_limit:
            return "time_out"
                
        # Проверка состояния игрока
        if self.player.lives <= 0:
            return "game_over"
            
        return "playing"
    
    def draw(self, screen):
        screen.fill(BACKGROUND_COLOR)
        self.map.draw_map(screen)
        
        # Отрисовка врагов и игрока
        for enemy in self.enemies:
            enemy.draw(screen)
            
        self.player.draw(screen)
    