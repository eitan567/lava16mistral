import pygame
import random

# --- Constants and Variables ---
WIDTH, HEIGHT = 600, 400  # Screen dimensions
CELL_SIZE = 20
SNAKE_COLOR = (0, 255, 0)  # Green
FOOD_COLOR = (0, 0, 255)  # Blue
WALL_COLOR = (255, 0, 0)  # Red

# ... other constants and variables (e.g., initial snake length, speed, etc.)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()  # For controlling game speed

def display_score():
    score_text = score_font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))  # Display score at (10, 10)

# --- Menu Functions ---
def display_menu():
    screen.fill((0, 0, 0))  # Clear the screen with black
    font = pygame.font.SysFont(None, 48)  # Choose a font

    # Render menu options
    options = ["Start New Game", "High Scores", "Exit"]
    y_pos = HEIGHT // 2 - len(options) * 50  # Calculate starting y position 

    for i, option in enumerate(options):
        text_surface = font.render(option, True, (255, 255, 255))  # White text
        text_rect = text_surface.get_rect(center=((WIDTH // 2), y_pos))

        # Highlight the currently selected option 
        if i == current_option:
            pygame.draw.rect(screen, (255, 0, 0), text_rect.inflate(20, 10), 3)  # Red outline

        screen.blit(text_surface, text_rect)
        y_pos += 60  # Move down for the next option

    pygame.display.flip()  # Update the display

def navigate_menu(current_option):
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                current_option = (current_option - 1) % 3  # Wrap around
            elif event.key == pygame.K_DOWN:
                current_option = (current_option + 1) % 3                
            elif event.key == pygame.K_RETURN:
                select_option(current_option)
    return current_option

def select_option(current_option):
    if current_option == 0:
        initialize_game()  # Start game
        game_loop()
    elif current_option == 1:
        # Display high scores (Implementation not shown)
        pass  # You'll need to implement this part to display high scores
    elif current_option == 2:
        pygame.quit()  # Exit game
        exit()

def initialize_game():
    global snake, food_pos, score, lives, snake_direction
    
    # Randomize the initial position of the snake within the playable area
    initial_x = 300 #random.randrange(CELL_SIZE, WIDTH - CELL_SIZE, CELL_SIZE)
    initial_y = 200 #random.randrange(CELL_SIZE, HEIGHT - CELL_SIZE, CELL_SIZE)
    
    snake = [(initial_x, initial_y)]  # Snake starts at the random position
    snake_direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])  # Random initial direction
    generate_food()  # Place the first food
    
def draw_game():
    screen.fill((0, 0, 0))  # Clear the screen with black

    # Draw walls
    pygame.draw.rect(screen, WALL_COLOR, (0, 0, WIDTH, CELL_SIZE))  # Top wall
    pygame.draw.rect(screen, WALL_COLOR, (0, 0, CELL_SIZE, HEIGHT))  # Left wall
    pygame.draw.rect(screen, WALL_COLOR, (0, HEIGHT - CELL_SIZE, WIDTH, CELL_SIZE))  # Bottom wall 
    pygame.draw.rect(screen, WALL_COLOR, (WIDTH - CELL_SIZE, 0, CELL_SIZE, HEIGHT))  # Right wall

    # Draw snake
    for segment in snake:
        x, y = segment
        pygame.draw.rect(screen, SNAKE_COLOR, (x, y, CELL_SIZE, CELL_SIZE))

    # Draw food
    pygame.draw.rect(screen, FOOD_COLOR, (food_pos[0], food_pos[1], CELL_SIZE, CELL_SIZE))

    pygame.display.flip()  # Update the display

def update_snake():
    global snake, food_pos, score, lives

    new_head = list(snake[0])  # Convert the head tuple to a list

    if snake_direction == "UP":
        new_head[1] -= CELL_SIZE
    elif snake_direction == "DOWN":
        new_head[1] += CELL_SIZE
    elif snake_direction == "LEFT":
        new_head[0] -= CELL_SIZE
    elif snake_direction == "RIGHT":
        new_head[0] += CELL_SIZE

    # Print for debugging
    print("New Head:", new_head)
    print("Snake Body:", snake[1:])

    # Check for collisions with walls
    if (
        new_head[0] < 0
        or new_head[0] >= WIDTH
        or new_head[1] < 0
        or new_head[1] >= HEIGHT
    ):
        lives -= 1  # Lose a life
        if lives == 0:
            game_over()  # Game over if no lives left
        else:
            initialize_game()  # Reset the game
    # Check for collisions with snake's body
    elif any(new_head == segment for segment in snake[1:]):
        lives -= 1  # Lose a life
        if lives == 0:
            game_over()  # Game over if no lives left
        else:
            initialize_game()  # Reset the game
    else:
        snake.insert(0, tuple(new_head))  # Insert new head

        # Check if snake ate food
        if abs(new_head[0] - food_pos[0]) <= 1 and abs(new_head[1] - food_pos[1]) <= 1:
            score += 1
            generate_food()
        else:
            snake.pop()  # Remove tail if no food was eaten




def generate_food():
    global food_pos
    while True:
        # Generate random positions within the playable area, excluding the area occupied by the walls
        food_x = random.randrange(CELL_SIZE, WIDTH - CELL_SIZE, CELL_SIZE)
        food_y = random.randrange(CELL_SIZE, HEIGHT - CELL_SIZE, CELL_SIZE)
        food_pos = (food_x, food_y)
        if food_pos not in snake:
            break  # Exit loop if food doesn't overlap with snake

def handle_input():
    global snake_direction
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_direction != "DOWN":
                snake_direction = "UP"
            elif event.key == pygame.K_DOWN and snake_direction != "UP":
                snake_direction = "DOWN"
            elif event.key == pygame.K_LEFT and snake_direction != "RIGHT":
                snake_direction = "LEFT"
            elif event.key == pygame.K_RIGHT and snake_direction != "LEFT":
                snake_direction = "RIGHT"

def game_over():    
    font = pygame.font.SysFont(None, 72)
    text_surface = font.render('Game Over', True, (255, 0, 0))
    text_rect = text_surface.get_rect(center=((WIDTH//2), (HEIGHT//2)))
    screen.blit(text_surface, text_rect)
    pygame.display.flip()
    pygame.time.wait(3000)  # Wait for 3 seconds
    display_menu()  # Return to main menu

# --- Main Game Loop ---
def game_loop():
    global score,lives
    score = 0
    lives = 3  # Set initial number of lives

    while lives>0:  # Main game loop
        clock.tick(5)
        handle_input()
        update_snake() 
        draw_game()
        display_score()
        # ... other game logic (e.g., check for game over conditions)
        pygame.display.update()  # Update the display

# --- Initialization ---
# Draw initial state of the game
initialize_game()
draw_game()
pygame.display.update()

# --- Main Menu --- 
current_option = 0  # Initially highlight the first option
score_font = pygame.font.SysFont(None, 36)
while True:
    display_menu()
    current_option = navigate_menu(current_option)

    # Get events and check for ENTER key press
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                select_option(current_option)

pygame.quit()  # Quit Pygame
