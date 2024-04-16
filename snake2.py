import pygame
import sys
import random
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 640, 480
CELL_SIZE = 20
SNAKE_SPEED = 15
FOOD_SPAWN_RATE = 1000
FONT_NAME = pygame.font.get_default_font()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (213, 50, 80)
BLUE = (50, 153, 213)
YELLOW = (255, 255, 102)

# Initialize game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

class Snake:
    def __init__(self):
        self.body = [(CELL_SIZE * 2, CELL_SIZE * 2),
                     (CELL_SIZE, CELL_SIZE)]
        self.direction = (0, 0)
        self.grow = False

    def move(self):
        head = self.body[0]
        if self.direction == (1, 0):
            new_head = (head[0], head[1] + CELL_SIZE)
        elif self.direction == (-1, 0):
            new_head = (head[0], head[1] - CELL_SIZE)
        elif self.direction == (0, 1):
            new_head = (head[0] + CELL_SIZE, head[1])
        elif self.direction == (0, -1):
            new_head = (head[0] - CELL_SIZE, head[1])

        self.body.insert(0, new_head)
        if not self.grow and len(self.body) > 2:
            del self.body[-1]
    
    def add_segment(self, old_head):
        self.body.insert(0, list(old_head))

        if len(self.body) > SNAKE_LENGTH:
            self.body.pop()

    def check_collisions(self):
        # Check for collisions with walls and itself
        head = self.body[0]
        if (head[0] in [0, WIDTH - CELL_SIZE]) or \
           (head[1] in [0, HEIGHT - CELL_SIZE]):
            pygame.quit()
            sys.exit()
        for segment in self.body[1:]:
            if head == segment:
                pygame.quit()
                sys.exit()

    def draw(self, surface):
        for segment in self.body:
            pygame.draw.rect(surface, WHITE, (segment[0], segment[1], CELL_SIZE, CELL_SIZE))

class Food:
    def __init__(self, surface):
        self.pos = [random.randint(CELL_SIZE * 2, WIDTH - CELL_SIZE * 2),
                    random.randint(CELL_SIZE * 2, HEIGHT - CELL_SIZE * 2)]
        self.size = random.randint(1, 3)
        self.grow = False
        self.surface = surface

    def draw(self):
        pygame.draw.rect(self.surface, RED, (self.pos[0], self.pos[1], CELL_SIZE * self.size, CELL_SIZE * self.size))

    def check_collisions(self, snake):
        if snake.body[0] == (self.pos[0], self.pos[1]):
            self.grow = True

    def spawn_new_food(self):
        self.pos = [random.randint(CELL_SIZE * 2, WIDTH - CELL_SIZE * 2),
                    random.randint(CELL_SIZE * 2, HEIGHT - CELL_SIZE * 2)]
        self.size = random.randint(1, 3)
        self.grow = False

def main():
    snake = Snake()
    food = Food(screen)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        
        if snake.body[0] == food.pos:
            food.spawn_new_food()
            snake.grow = True
            new_head = [snake.body[0][0], snake.body[0][1]]
            snake.add_segment(new_head)
        
        screen.fill(BLACK)
        snake.move()
        snake.check_collisions()
        snake.draw(screen)
        food.draw(screen)

        pygame.display.flip()
        clock.tick(SNAKE_SPEED)

if __name__ == "__main__":
    main()