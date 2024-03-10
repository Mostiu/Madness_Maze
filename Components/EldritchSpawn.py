import random
from Config import *
import pygame
from collections import deque
class EldritchSpawn:
    def __init__(self, maze):
        self.x = random.randint(0, maze.width - 1)
        self.y = random.randint(0, maze.height - 1)
        self.width = CELL_SIZE
        self.height = CELL_SIZE
        self.maze = maze

    def draw(self, screen):
        if self.maze.visited[self.y][self.x]:
            pygame.draw.rect(screen, GREEN, (self.x * CELL_SIZE, self.y * CELL_SIZE, self.width, self.height))

    def bfs_path(self, start, goal):
        queue = deque([[start]])  # Queue of paths
        visited = set([start])
        while queue:
            path = queue.popleft()
            x, y = path[-1]

            # Check if we've reached the goal
            if (x, y) == goal:
                return path

            # Explore neighbors
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.maze.width and 0 <= ny < self.maze.height and self.maze.maze[ny][nx] == 1 and (
                        nx, ny) not in visited:
                    visited.add((nx, ny))
                    new_path = list(path)
                    new_path.append((nx, ny))
                    queue.append(new_path)
        return None  # No path found

    def move_towards_player(self, player_x, player_y):
        start = (self.x, self.y)
        goal = (player_x, player_y)
        path = self.bfs_path(start, goal)
        if path and len(path) > 1:
            next_step = path[1]
            self.x, self.y = next_step

    def move_randomly(self):
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(directions)

        for dx, dy in directions:
            new_x, new_y = self.x + dx, self.y + dy
            if 0 <= new_x < self.maze.width and 0 <= new_y < self.maze.height and self.maze.maze[new_y][new_x] == 1:
                self.x = new_x
                self.y = new_y
                break
