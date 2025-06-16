import pygame
from config import *
from tilemap import *
from animations import *

class Collisions:
    def get_hits(self, tiles):
        hits = []
        for tile in tiles:
            if self.rect.colliderect(tile):
                hits.append(tile)
        return hits
    
    def check_collisions_x(self, tiles):
        collisions = self.get_hits(tiles)
        for tile in collisions:
            if self.velocity.x > 0:  
                self.position.x = tile.rect.left - self.rect.w
                self.rect.x = self.position.x
            elif self.velocity.x < 0:  
                self.position.x = tile.rect.right
                self.rect.x = self.position.x

    def check_collisions_y(self, tiles):
        self.on_ground = False
        self.rect.bottom += 1
        collisions = self.get_hits(tiles)
        for tile in collisions:
            if self.velocity.y > 0:  
                self.on_ground = True
                self.is_jumping = False
                self.velocity.y = 0
                self.position.y = tile.rect.top
                self.rect.bottom = self.position.y
            elif self.velocity.y < 0: 
                self.velocity.y = 0
                self.position.y = tile.rect.bottom + self.rect.h
                self.rect.bottom = self.position.y

class Player(pygame.sprite.Sprite, Collisions):
    def __init__(self, enemies_group):
        pygame.sprite.Sprite.__init__(self)
        self.animations = CharacterAnimations('player')
        self.image = self.animations.get_image()
        self.LEFT_KEY, self.RIGHT_KEY = False, False
        self.FACING_LEFT = False
        self.is_jumping, self.on_ground = False, False
        self.gravity, self.friction = .35, -.12 #гравитация и трение
        self.enemies = enemies_group 
        self.rect = self.image.get_rect()
        
        self.position, self.velocity = pygame.math.Vector2(0,0), pygame.math.Vector2(0,0)
        self.acceleration = pygame.math.Vector2(0,self.gravity)
        self.is_attacking = False
        self.attack_cooldown = 0 #кд атаки
        self.attack_range = 20  # дистанция атаки
        self.attack_duration = 15  # длительность атаки в кадрах
        self.attack_hitbox = None
        self.killed_enemies = [] 

        self.max_hp = 3
        self.hp = self.max_hp

    def draw(self, display):
        display.blit(self.image, (self.rect.x, self.rect.y))

    def update(self, dt, tiles, enemies):
        if self.hp <= 0:
            return
        # обновляем анимацию под действие
        state = {
            'moving_left': self.LEFT_KEY,
            'moving_right': self.RIGHT_KEY,
            'jumping': self.is_jumping or not self.on_ground,
            'on_ground': self.on_ground,
            'attacking': self.is_attacking
        }
        self.animations.update_animation(state)
        self.image = self.animations.get_image()
        
        self.update_facing_direction()
        self.horizontal_movement(dt)
        self.check_collisions_x(tiles)
        self.vertical_movement(dt)
        self.check_collisions_y(tiles)

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
            
        if self.is_attacking:
            if self.attack_duration > 0:
                self.attack_duration -= 1
                self.check_attack_hit(enemies)
            else:
                self.is_attacking = False
                self.attack_duration = 15
                self.attack_hitbox = None

        if self.position.y > SCREEN_HEIGHT:
            self.hp -= 1
            if self.lives > 0:
                self.respawn()
                return
        
    def update_facing_direction(self): #для хитбокса атаки нужно
        if self.LEFT_KEY and not self.RIGHT_KEY:
            self.FACING_LEFT = True
        elif self.RIGHT_KEY and not self.LEFT_KEY:
            self.FACING_LEFT = False
        
    def horizontal_movement(self, dt):
        self.acceleration.x = 0
        if self.LEFT_KEY:
            self.acceleration.x -= .3
        elif self.RIGHT_KEY:
            self.acceleration.x += .3
        self.acceleration.x += self.velocity.x * self.friction
        self.velocity.x += self.acceleration.x * dt
        self.limit_velocity(4)
        self.position.x += self.velocity.x * dt + (self.acceleration.x * .5) * (dt * dt)
        self.rect.x = self.position.x

    def vertical_movement(self, dt):
        self.velocity.y += self.acceleration.y * dt
        if self.velocity.y > 7: self.velocity.y = 7
        self.position.y += self.velocity.y * dt + (self.acceleration.y * .5) * (dt * dt)
        self.rect.bottom = self.position.y

    def limit_velocity(self, max_vel):
        self.velocity.x = max(-max_vel, min(self.velocity.x, max_vel))
        if abs(self.velocity.x) < .01: self.velocity.x = 0

    def jump(self):
        if self.on_ground:
            self.is_jumping = True
            self.velocity.y -= 9.9
            self.on_ground = False

    def attack(self):
        if not self.is_attacking and self.attack_cooldown == 0:
            self.is_attacking = True
            self.attack_cooldown = 30 
            
            #хитбокс атаки чтобы можно было бить в обе стороны
            if self.FACING_LEFT:
                self.attack_hitbox = pygame.Rect(
                    self.rect.left - self.attack_range, 
                    self.rect.top,
                    self.attack_range,
                    self.rect.height
                )
            else:
                self.attack_hitbox = pygame.Rect(
                    self.rect.right, 
                    self.rect.top,
                    self.attack_range,
                    self.rect.height
                )

    def check_attack_hit(self, enemies):
        if not self.attack_hitbox:
            return
            
        for enemy in list(enemies):
            if enemy.alive and self.attack_hitbox.colliderect(enemy.rect):
                enemy.alive = False
                enemy.respawn_timer = 0
                enemy.death_time = pygame.time.get_ticks()
                self.killed_enemies.append(enemy) #временный список убитых, позже будет использован для счета
                self.is_attacking = False
                self.attack_hitbox = None
                break

    def respawn(self):
        self.position = pygame.math.Vector2(START_POSITION_LVL_1[0], START_POSITION_LVL_1[1])
        self.velocity = pygame.math.Vector2(0, 0)
        self.rect.x = self.position.x
        self.rect.y = self.position.y
        
        for enemy in (self.enemies):
            enemy.alive = True
            enemy.respawn()


class Enemy(pygame.sprite.Sprite, Collisions):
   
    def __init__(self, x, y, speed=1, patrol_distance=150):
        pygame.sprite.Sprite.__init__(self)
        self.animations = CharacterAnimations('enemy')
        self.image = self.animations.get_image()
        self.rect = self.image.get_rect()
        self.start_x = x
        self.start_y = y
        self.position = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0, 0.35)
        self.speed = speed
        self.direction = 1
        self.patrol_distance = patrol_distance
        self.on_ground = False
        self.friction = -0.12
        self.platform_left = 0 
        self.platform_right = 0 
        self.initialized = False
        self.falling_check_distance = 20 
        self.alive = True
        self.respawn_timer = 0
        self.respawn_delay = 200

    def update(self, dt, player, tiles):

        state = {
            'moving_left': self.direction < 0,
            'moving_right': self.direction > 0,
            'on_ground': self.on_ground,
        }
        
        self.animations.update_animation(state)
        self.image = self.animations.get_image()
        current_time = pygame.time.get_ticks()
        if not self.alive:
            if current_time - self.death_time >= self.respawn_delay:
                self.respawn()
            return
        
        if not self.initialized and self.on_ground:
            self.find_platform_edges(tiles)
            self.initialized = True

        self.vertical_movement(dt)
        self.check_collisions_y(tiles)
    

        self.horizontal_movement(dt)
        self.check_collisions_x(tiles)
    
        if self.initialized and self.on_ground:
            self.check_for_ledge(tiles)

        if self.rect.colliderect(player.rect):
            player.hp -= 1
            if player.hp > 0:
                player.respawn()

    def respawn(self):
        self.position = pygame.math.Vector2(self.start_x, self.start_y)
        self.velocity = pygame.math.Vector2(0, 0)
        self.rect.x = self.start_x
        self.rect.y = self.start_y
        self.direction = 1
        self.alive = True
        self.initialized = False
        self.on_ground = False
        self.respawn_timer = 0
     
    #следующие 2 функции нужны, чтобы враг не падал с патрулируемой платформы и ходил от одного края к другому
    def find_platform_edges(self, tiles):
        ground_tiles = [t for t in tiles if t.rect.top == self.rect.bottom]
        
        if ground_tiles:
            
            left_edges = [t.rect.left for t in ground_tiles]
            right_edges = [t.rect.right for t in ground_tiles]
            
            self.platform_left = min(left_edges)
            self.platform_right = max(right_edges)
            

            self.patrol_left_bound = max(self.platform_left, self.position.x - self.patrol_distance/2)
            self.patrol_right_bound = min(self.platform_right, self.position.x + self.patrol_distance/2)

    def check_for_ledge(self, tiles):
  
        check_x = self.rect.left - 10 if self.direction == -1 else self.rect.right + 10
        check_rect = pygame.Rect(check_x, self.rect.bottom, 1, self.falling_check_distance)
        
        has_ground = False
        for tile in tiles:
            if check_rect.colliderect(tile.rect):
                has_ground = True
                break
        
        if not has_ground:
            self.direction *= -1  

    def horizontal_movement(self, dt):
        if not self.initialized:
            return
            
        self.acceleration.x = self.speed * self.direction
        self.acceleration.x += self.velocity.x * self.friction
        self.velocity.x += self.acceleration.x * dt
        self.limit_velocity(self.speed)
        self.position.x += self.velocity.x * dt
        self.rect.x = self.position.x

        if self.position.x < self.platform_left:
            self.position.x = self.platform_left
            self.direction = 1 
            
        elif self.position.x + self.rect.width > self.platform_right:
            self.position.x = self.platform_right - self.rect.width
            self.direction = -1 


    def vertical_movement(self, dt):
        self.velocity.y += self.acceleration.y * dt
        if self.velocity.y > 7: 
            self.velocity.y = 7
        self.position.y += self.velocity.y * dt
        self.rect.y = self.position.y
    

    def limit_velocity(self, max_vel): #ограничение ускорения для плавного движения
        self.velocity.x = max(-max_vel, min(self.velocity.x, max_vel))
        if abs(self.velocity.x) < .01: 
            self.velocity.x = 0


    def draw(self, display):
        if self.alive:
            display.blit(self.image, (self.rect.x, self.rect.y))