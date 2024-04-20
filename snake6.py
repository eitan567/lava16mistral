import pygame
import time
import random

pygame.init()

white = (255, 255, 255)
yellow = (255, 255, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)


dis_width = 800
dis_height = 600

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game')

clock = pygame.time.Clock()

snake_block = 10
snake_speed = 15

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 30)

def your_score(score):
    display_text = score_font.render("Your Score: " + str(score), True, yellow)
    dis.blit(display_text, [0, 0])

def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, white, [x[0], x[1], snake_block, snake_block])
    pygame.display.update()

def message_to_screen(msg, color):
    screen_text = font_style.render(msg, True, color)
    dis.blit(screen_text, [dis_width / 6, dis_height / 3])

def gameLoop():
    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snack_x = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    snack_y = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    snake_List = []
    Length_of_snake = 1

    while not game_over:

        while game_close:
            dis.fill(blue)
            message_to_screen("You Lost! Press C-Play Again or Q-Quit", red)
            your_score(Length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    elif event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        dis.fill(blue)
        pygame.draw.rect(dis, green, [snack_x, snack_y, snake_block, snake_block])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)

        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)

        pygame.display.update()

        if x1 == snack_x and y1 == snack_y:
            Length_of_snake += 1
            snack_x = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            snack_y = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()