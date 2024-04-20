import pygame
import time
import random
pygame.init()

# Define colors
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Game window setup
dis_width = 600
dis_height = 400
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game')

clock = pygame.time.Clock()
snake_speed = 15

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])

def gameLoop():
    game_over = False
    game_close = False
    snake_dir="NONE"

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_Block = 10
    snake_list = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, dis_width - snake_Block) / 10.0) * 10.0
    fody = round(random.randrange(0, dis_height - snake_Block) / 10.0) * 10.0

    while not game_over:

        while game_close == True:
            dis.fill(blue)
            message("You lost! Press Q-Quit or C-Play Again", red)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and snake_dir!="RIGHT":
                    x1_change = -snake_Block
                    y1_change = 0
                    snake_dir="LEFT"
                elif event.key == pygame.K_RIGHT and snake_dir!="LEFT":
                    x1_change = snake_Block
                    y1_change = 0
                    snake_dir="RIGHT"
                elif event.key == pygame.K_UP and snake_dir!="DOWN":
                    y1_change = -snake_Block
                    x1_change = 0
                    snake_dir="UP"
                elif event.key == pygame.K_DOWN and snake_dir!="UP":
                    y1_change = snake_Block
                    x1_change = 0
                    snake_dir="DOWN"

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
        else:
            x1 += x1_change
            y1 += y1_change
            dis.fill(blue)
            pygame.draw.rect(dis, green, [foodx, fody, snake_Block, snake_Block])
            snake_Head = []
            snake_Head.append(x1)
            snake_Head.append(y1)
            snake_list.append(snake_Head)

            if len(snake_list) > Length_of_snake:
                del snake_list[0]

            for x in snake_list[:-1]:
                pygame.draw.rect(dis, black, [x[0], x[1], snake_Block, snake_Block])

            our_snake(snake_Block, snake_list)

        pygame.display.update()

        if x1 == foodx and y1 == fody:
            foodx = round(random.randrange(0, dis_width - snake_Block) / 10.0) * 10.0
            fody = round(random.randrange(0, dis_height - snake_Block) / 10.0) * 10.0
            Length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()