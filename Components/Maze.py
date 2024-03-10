import random
import math
from Config import *
import pygame
class Maze:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.maze = [[0 for _ in range(width)] for _ in range(height)]
        self.exit_x, self.exit_y = 0, 0
        self.visited = [[False for _ in range(width)] for _ in range(height)]

    def generate(self):
        def carve_passages_from(x, y):
            directions = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
            random.shuffle(directions)

            for (nx, ny) in directions:
                if 0 <= nx < self.width and 0 <= ny < self.height and self.maze[ny][nx] == 0:
                    if sum([self.maze[ny + dy][nx + dx] for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)] if
                            0 <= nx + dx < self.width and 0 <= ny + dy < self.height]) < 2:
                        self.maze[y][x], self.maze[ny][nx] = 1, 1
                        carve_passages_from(nx, ny)

        self.maze[START_Y][START_X] = 1
        carve_passages_from(START_X, START_Y)
        self.place_exit(START_X, START_Y)
        self.update_visibility(self.exit_x, self.exit_y, 5)
        self.add_extra_paths()

    def add_extra_paths(self):
        extra_paths_count = int((self.width * self.height) * 0.05)  # Example: Add paths equal to 5% of the cells

        for _ in range(extra_paths_count):
            x, y = random.randint(0, self.width - 2), random.randint(0, self.height - 2)
            if self.maze[y][x] == 0 and self.maze[y][x + 1] == 1:
                self.maze[y][x] = 1  # Carve an additional path

    def place_exit(self, player_start_x, player_start_y):
        max_distance = 0
        for y in range(self.height):
            for x in range(self.width):
                if self.maze[y][x] == 1:
                    distance = math.sqrt((player_start_x - x) ** 2 + (player_start_y - y) ** 2)
                    if distance > max_distance:
                        max_distance = distance
                        self.exit_x, self.exit_y = x, y

    def update_visibility(self, x, y, radius):
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                new_x, new_y = x + dx, y + dy
                if 0 <= new_x < self.width and 0 <= new_y < self.height:
                    if math.sqrt(dx ** 2 + dy ** 2) <= radius:
                        self.visited[new_y][new_x] = True

    def draw(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                if self.visited[y][x]:  # Check if the cell has been visited
                    color = WHITE if self.maze[y][x] == 1 else BLACK
                    if x == self.exit_x and y == self.exit_y:
                        color = GOLD
                else:
                    color = GRAY
                pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

