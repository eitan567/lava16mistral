import pygame
import random

# Initialize pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Snake initial position and properties
snake_pos = [WIDTH // 2, HEIGHT // 2]
snake_body = [[WIDTH // 2, HEIGHT // 2], [WIDTH // 2 - 10, HEIGHT // 2], [WIDTH // 2 - 20, HEIGHT // 2]]
snake_dir = "RIGHT"

# Food position and properties
food_pos = [random.randrange(1, (WIDTH//10)) * 10, random.randrange(1, (HEIGHT//10)) * 10]
food_spawn = True

# Score and strikes
score = 0
strikes = 3
font = pygame.font.Font(None, 36)

# Startup screen
def show_startup_screen():
    global snake_pos, snake_body, snake_dir, food_pos, food_spawn, score, strikes
    startup = True
    while startup:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    startup = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

        screen.fill(BLACK)
        title_font = pygame.font.Font(None, 64)
        title = title_font.render("Snake Game", True, GREEN)
        title_rect = title.get_rect(center=(WIDTH/2, HEIGHT/4))
        screen.blit(title, title_rect)

        play_font = pygame.font.Font(None, 36)
        play_text = play_font.render("Press SPACE to play", True, GREEN)
        play_rect = play_text.get_rect(center=(WIDTH/2, HEIGHT/2))
        screen.blit(play_text, play_rect)

        pygame.display.flip()
        clock.tick(15)

# Main game loop
clock = pygame.time.Clock()
show_startup_screen()
game_over = False
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            # Use an if-else structure to prevent immediate direction reversal
            if event.key == pygame.K_UP and snake_dir != "DOWN":
                snake_dir = "UP"
            elif event.key == pygame.K_DOWN and snake_dir != "UP":
                snake_dir = "DOWN"
            elif event.key == pygame.K_LEFT and snake_dir != "RIGHT":
                snake_dir = "LEFT"
            elif event.key == pygame.K_RIGHT and snake_dir != "LEFT":
                snake_dir = "RIGHT"

    # Correctly calculate the new position of the snake's head
    if snake_dir == "UP":
        snake_pos[1] -= 10  # Move up
    elif snake_dir == "DOWN":
        snake_pos[1] += 10  # Move down
    elif snake_dir == "LEFT":
        snake_pos[0] -= 10  # Move left
    elif snake_dir == "RIGHT":
        snake_pos[0] += 10  # Move right
    # Move the snake
    new_pos = [snake_pos[0] ,
               snake_pos[1]]

    # Check for food collision
    if new_pos[0] == food_pos[0] and new_pos[1] == food_pos[1]:
        score += 1
        food_spawn = False
    else:
        snake_body.pop(0)

    # Check for wall collision
    if new_pos[0] < 0 or new_pos[0] >= WIDTH or new_pos[1] < 0 or new_pos[1] >= HEIGHT:
        strikes -= 1
        if strikes == 0:
            game_over = True
        else:
            show_startup_screen()

    # Check for self-collision
    if new_pos in snake_body:
        strikes -= 1
        if strikes == 0:
            game_over = True
        else:
            show_startup_screen()

    # Update snake position and add new segment
    snake_pos = new_pos
    snake_body.append(list(snake_pos))

    # Spawn food if it's not already there
    if not food_spawn:
        food_pos = [random.randrange(1, (WIDTH//10)) * 10, random.randrange(1, (HEIGHT//10)) * 10]
        food_spawn = True

    # Clear screen
    screen.fill(BLACK)

    # Draw food
    pygame.draw.rect(screen, GREEN, (food_pos[0], food_pos[1], 10, 10))

    # Draw snake
    for pos in snake_body:
        pygame.draw.rect(screen, GREEN, (pos[0], pos[1], 10, 10))

    # Draw score and strikes
    score_text = font.render("Score: " + str(score), True, RED)
    strike_text = font.render("Strikes: " + str(strikes), True, RED)
    screen.blit(score_text, (10, 10))
    screen.blit(strike_text, (WIDTH - strike_text.get_width() - 10, 10))

    pygame.display.flip()
    clock.tick(8)

# Exit pygame
pygame.quit()