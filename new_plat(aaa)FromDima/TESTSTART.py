import pygame
from player import Player, Enemy
from config import *
from spritesheet import Spritesheet
from tilemap import *

from Music import *
from Screens import *
#pip install -r requirements.txt для установки пакетов из файла, необходимых для игры
def main():
    pygame.init()
    audio_manager = AudioManager()
    
    # Инициализация экранов
    start_screen = StartScreen(SCREEN_WIDTH, SCREEN_HEIGHT, audio_manager)
    dead_screen = DeadScreen(SCREEN_WIDTH, SCREEN_HEIGHT, audio_manager)
    level_complete_screen = LevelCompleteScreen(SCREEN_WIDTH, SCREEN_HEIGHT, audio_manager, 0)
    final_screen = FinalScreen(SCREEN_WIDTH, SCREEN_HEIGHT, audio_manager)
    
    # Главное меню
    if not start_screen.run():
        pygame.quit()
        return
    
    # Игровые переменные
    screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    spritesheet = Spritesheet('spritesheet.png')
    map = TileMap('level_1.csv', spritesheet)
    
    # Создание игровых объектов
    enemies = pygame.sprite.Group()
    enemy_positions = [(300, 420), (350, 270), (700, 420)]
    for pos in enemy_positions:
        enemies.add(Enemy(*pos))
        
    player = Player(enemies)
    player.position.x, player.position.y = START_POSITION_LVL_1

    clock = pygame.time.Clock()
    running = True
    TARGET_FPS = 60
    current_level = 1
    
    # Основной игровой цикл
    while running:
        dt = clock.tick(60) * 0.001 * TARGET_FPS
        
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Обработка клавиш управления
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    player.LEFT_KEY = True
                elif event.key == pygame.K_d:
                    player.RIGHT_KEY = True
                elif event.key == pygame.K_SPACE:
                    player.jump()
                    audio_manager.play('jump')
                elif event.key == pygame.K_f: 
                    player.attack()
                    audio_manager.play('hit')
                # Тестовые клавиши
                elif event.key == pygame.K_i:  # Экран смерти
                    dead_result = dead_screen.run()
                    if dead_result:  # Перезапуск уровня
                        player.position.x, player.position.y = START_POSITION_LVL_1
                        enemies.empty()
                        for pos in enemy_positions:
                            enemies.add(Enemy(*pos))
                    else:  # Выход
                        running = False
                elif event.key == pygame.K_o:  # Экран завершения уровня
                    level_result = level_complete_screen.run()
                    if level_result:  # Следующий уровень
                        current_level += 1
                        # Здесь должна быть загрузка нового уровня
                        player.position.x, player.position.y = START_POSITION_LVL_1
                        enemies.empty()
                        for pos in enemy_positions:
                            enemies.add(Enemy(*pos))
                    else:  # Выход
                        running = False
                elif event.key == pygame.K_p:  # Финальный экран
                    final_result = final_screen.run()
                    if final_result == "menu":  # В главное меню
                        if start_screen.run():
                            # Перезапуск игры
                            player.position.x, player.position.y = START_POSITION_LVL_1
                            enemies.empty()
                            for pos in enemy_positions:
                                enemies.add(Enemy(*pos))
                            current_level = 1
                        else:
                            running = False
                    else:  # Выход
                        running = False
                        
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    player.LEFT_KEY = False
                elif event.key == pygame.K_d:
                    player.RIGHT_KEY = False
                elif event.key == pygame.K_SPACE:
                    if player.is_jumping:
                        player.velocity.y *= .25
                        player.is_jumping = False
        
        # Управление звуком шагов
        if not player.is_jumping:
            if (player.LEFT_KEY or player.RIGHT_KEY):
                audio_manager.play_run()
            else:
                audio_manager.stop_run()
        else:
            audio_manager.stop_run()
        
        # Обновление игровых объектов
        player.update(dt, map.tiles, enemies)
        for enemy in enemies:
            enemy.update(dt, player, map.tiles)
        
        # Отрисовка
        screen.fill(BACKGROUND_COLOR)  
        map.draw_map(screen)
        for enemy in enemies:
            enemy.draw(screen)
        player.draw(screen)
        
        window.blit(screen, (0, 0)) 
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()