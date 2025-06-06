import pygame
from player import Player, Enemy
from config import *
from spritesheet import Spritesheet
from tilemap import *

#pip install -r requirements.txt для установки пакетов из файла, необходимых для игры

def main():
    pygame.init()
    screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    spritesheet = Spritesheet('spritesheet.png')
    
    # загрузка карты
    map = TileMap('test_level.csv', spritesheet)
    
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
                elif event.key == pygame.K_f: 
                    player.attack()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    player.LEFT_KEY = False
                elif event.key == pygame.K_d:
                    player.RIGHT_KEY = False
                elif event.key == pygame.K_SPACE:
                    if player.is_jumping:
                        player.velocity.y *= .25
                        player.is_jumping = False
        
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
