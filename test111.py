import pygame
#test
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500
PLAYER_SPEED = 9 
BACKGROUND_COLOR = (207, 229, 250) 
PLAYER_COLOR = (120, 94, 130) 

class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        self.image = pygame.Surface((200, 200))
        self.image.fill(PLAYER_COLOR) 

        self.rect = self.image.get_rect()

        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 20 

        self.change_x = 0
        self.change_y = 0

        self.facing_right = True

    def update(self):

        self.rect.x += self.change_x

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

        self.rect.y += self.change_y

        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


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

    def go_up(self):
        self.change_y = -PLAYER_SPEED

    def go_down(self):
        self.change_y = PLAYER_SPEED

    def stop(self):
        self.change_x = 0
        self.change_y = 0 

    def flip(self):

        self.image = pygame.transform.flip(self.image, True, False)


def main():

    pygame.init()

    size = (SCREEN_WIDTH, SCREEN_HEIGHT)
    screen = pygame.display.set_mode(size) 

    pygame.display.set_caption("movement")

    player = Player()

    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

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
                elif event.key == pygame.K_w:
                    player.go_up()
                elif event.key == pygame.K_s:
                    player.go_down()
                elif event.key == pygame.K_ESCAPE: 
                    running = False
            elif event.type == pygame.KEYUP: 
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    player.stop()
                elif event.key == pygame.K_w or event.key == pygame.K_s:
                    player.stop()

        all_sprites.update() 

        screen.fill(BACKGROUND_COLOR) 

        all_sprites.draw(screen) 


        pygame.display.flip()

        clock.tick(60) 

    pygame.quit()

if __name__ == "__main__":
    main()
