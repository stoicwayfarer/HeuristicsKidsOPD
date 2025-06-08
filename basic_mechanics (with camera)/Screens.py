import pygame
from config import *

def start_screen():
    global SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE
    pygame.init()
    start_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("COFFEFU")

    background = pygame.image.load("Images&Sprites/Test.Fon.jpg").convert()
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT)) 

    #шрифт
    title_font = pygame.font.Font('Fonts/MochiyPopOne-Regular.ttf', 54)
    developers_font = pygame.font.SysFont('Comic Sans MS',54)
    button_font = pygame.font.SysFont('Comic Sans MS', 36)

    title_text = title_font.render("COFFEFU", True, BLACK)
    developers_text= developers_font.render("Heuristics kids", True, BLACK)
    start_text = button_font.render("Начать игру", True, BLACK)
    exit_text = button_font.render("Выйти", True, BLACK)

    #прямоугольники для кнопок
    start_button = pygame.Rect(670, 300, 200, 50)
    exit_button = pygame.Rect(670, 499, 200, 50)

    running = True
    while running:
        start_screen.blit(background, (0, 0))

        start_screen.blit(title_text, (600,100)) 
        start_screen.blit(developers_text,(20,680))

        #отрисовка кнопок и текста
        button_surface = pygame.Surface((200, 50), pygame.SRCALPHA)
        button_surface.fill(WHITE)
        start_screen.blit(button_surface, (670, 300))
        start_screen.blit(button_surface, (670, 499))

        start_screen.blit(start_text, (670 + (200 - start_text.get_width()) // 2, 300+ (50 - start_text.get_height()) // 2))
        start_screen.blit(exit_text, (670 + (200 - exit_text.get_width()) // 2, 499 + (50 - exit_text.get_height()) // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_RETURN:
                    running = False
                    return True

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                if start_button.collidepoint(mouse_pos):
                    running = False
                    return True

                if exit_button.collidepoint(mouse_pos):
                    running = False
                    pygame.quit()
                    return False

    pygame.quit()
    return False


def dead_screen():
    global SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE
    pygame.init()
    start_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Вы проиграли :(")


    background = pygame.image.load("Images&Sprites/Test.Fon.jpg").convert() 
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT)) 

    title_font = pygame.font.SysFont('Comic Sans MS', 54)
    button_font = pygame.font.SysFont('Comic Sans MS', 36)

    title_text = title_font.render("Вы проиграли", True, BLACK)
    start_text = button_font.render("Начать снала", True, BLACK)
    exit_text = button_font.render("Выйти", True, BLACK)

    start_button = pygame.Rect(670, 300, 200, 50)
    exit_button = pygame.Rect(670, 499, 200, 50)

    running = True
    while running:
        start_screen.blit(background, (0, 0))

        start_screen.blit(title_text, (600,100)) 

        button_surface = pygame.Surface((200, 50), pygame.SRCALPHA)
        button_surface.fill(WHITE)
        start_screen.blit(button_surface, (670, 300))
        start_screen.blit(button_surface, (670, 499))

        start_screen.blit(start_text, (670 + (200 - start_text.get_width()) // 2, 300+ (50 - start_text.get_height()) // 2))
        start_screen.blit(exit_text, (670 + (200 - exit_text.get_width()) // 2, 499 + (50 - exit_text.get_height()) // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_RETURN:
                    running = False
                    return True

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                if start_button.collidepoint(mouse_pos):
                    running = False
                    return True

                if exit_button.collidepoint(mouse_pos):
                    running = False
                    pygame.quit()
                    return False

    pygame.quit()
    return False