import random
import pygame

MAZE_SCREEN_WIDTH, MAZE_SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((MAZE_SCREEN_WIDTH + 50, MAZE_SCREEN_HEIGHT))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GOLD = (255, 215, 0)
GRAY = (128, 128, 128)
GREEN = (0, 255, 0)

# Maze settings
CELL_SIZE = 20
MAZE_WIDTH, MAZE_HEIGHT = MAZE_SCREEN_WIDTH // CELL_SIZE, MAZE_SCREEN_HEIGHT // CELL_SIZE
START_X, START_Y = random.randrange(MAZE_WIDTH), random.randrange(MAZE_HEIGHT)
VISIBILITY_RATE = 7
