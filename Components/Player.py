from Config import *
import pygame
class Player:
    def __init__(self, x, y, maze):
        self.x = x
        self.y = y
        self.width = CELL_SIZE
        self.height = CELL_SIZE
        self.maze = maze
        self.visibility_radius = VISIBILITY_RATE
        self.maze.update_visibility(x, y, self.visibility_radius)

    def draw(self, screen):
        pygame.draw.rect(screen, RED, (self.x * CELL_SIZE, self.y * CELL_SIZE, self.width, self.height))

    def move(self, dx, dy):
        new_x, new_y = self.x + dx, self.y + dy
        if 0 <= new_x < MAZE_WIDTH and 0 <= new_y < MAZE_HEIGHT:
            if self.maze.maze[new_y][new_x] == 1:
                self.x = new_x
                self.y = new_y
                self.maze.update_visibility(new_x, new_y, self.visibility_radius)

