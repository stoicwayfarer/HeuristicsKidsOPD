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
    start_screen = StartScreen(SCREEN_WIDTH, SCREEN_HEIGHT, audio_manager)
    dead_screen = DeadScreen(SCREEN_WIDTH, SCREEN_HEIGHT, audio_manager)
    t=148
    level_complete_screen = LevelCompleteScreen(SCREEN_WIDTH, SCREEN_HEIGHT, audio_manager, t)
    final_screen = FinalScreen(SCREEN_WIDTH, SCREEN_HEIGHT, audio_manager)
    

    if not start_screen.run():
        return
    
    screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    spritesheet = Spritesheet('spritesheet.png')
    
    # загрузка карты
    map = TileMap('level_1.csv', spritesheet)
    
    enemies = pygame.sprite.Group()
    enemy_positions = [
        (300, 420),  
        (350, 270),
        (700, 420)
    ]
    
    # создание враговб позже будет в классе уровней
    for pos in enemy_positions:
        enemy = Enemy(*pos) 
        enemies.add(enemy)
        
    player = Player(enemies)
    player.position.x, player.position.y = START_POSITION_LVL_1

    clock = pygame.time.Clock()
    running = True
    TARGET_FPS = 60        
    while running:
        dt = clock.tick(60) * 0.001 * TARGET_FPS
        
        # обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
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
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    player.LEFT_KEY = False
                elif event.key == pygame.K_d:
                    player.RIGHT_KEY = False
                elif event.key == pygame.K_SPACE:
                    if player.is_jumping:
                        player.velocity.y *= .25
                        player.is_jumping = False
        
        if not player.is_jumping:
            if (player.LEFT_KEY or player.RIGHT_KEY):
                audio_manager.play_run()
            else:
                audio_manager.stop_run()
        else:
            audio_manager.stop_run()
        
        # обновление игрока
        player.update(dt, map.tiles, enemies)
        
        # обновление врагов
        for enemy in enemies:
            enemy.update(dt,player, map.tiles)
        
        # отрисовка
        screen.fill(BACKGROUND_COLOR)  
        map.draw_map(screen)  # рисуем карту
        
        # рисуем врагов
        for enemy in enemies:
            enemy.draw(screen)
            
        player.draw(screen)  # рисуем игрока
        
        window.blit(screen, (0, 0)) 
        pygame.display.update()  

    pygame.quit()

if __name__ == "__main__":
    main()