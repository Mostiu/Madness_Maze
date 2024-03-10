import pygame
import random
import math
from collections import deque
# Initialize Pygame
pygame.init()

# Screen dimensions


MAZE_SCREEN_WIDTH, MAZE_SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((MAZE_SCREEN_WIDTH+50, MAZE_SCREEN_HEIGHT))

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


class Maze:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.maze = [[0 for _ in range(width)] for _ in range(height)]
        self.exit_x, self.exit_y = 0, 0  # Exit tile coordinates
        self.visited = [[False for _ in range(width)] for _ in range(height)]  # Track visited cells

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
            # Move to the next step towards the player
            next_step = path[1]  # Get the next step towards the player
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


class Game:
    def __init__(self):
        self.maze = Maze(MAZE_WIDTH, MAZE_HEIGHT)
        self.maze.generate()
        self.player = Player(START_X, START_Y, self.maze)
        self.eldritch_spawn = EldritchSpawn(self.maze)

    def run(self):
        running = True
        clock = pygame.time.Clock()
        confused_timer = 10
        while running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.player.move(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        self.player.move(1, 0)
                    elif event.key == pygame.K_UP:
                        self.player.move(0, -1)
                    elif event.key == pygame.K_DOWN:
                        self.player.move(0, 1)
                    elif event.key == pygame.K_q:
                        confused_timer = 10

                    if confused_timer > 0:
                        self.eldritch_spawn.move_randomly()
                    else:
                        self.eldritch_spawn.move_towards_player(self.player.x, self.player.y)
                    confused_timer -= 1


            screen.fill(BLACK)
            self.maze.draw(screen)
            self.player.draw(screen)
            self.eldritch_spawn.draw(screen)
            pygame.display.flip()
            clock.tick(30)

        pygame.quit()




def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def main_menu():
    while True:
        screen.fill(BLACK)
        draw_text('Madness Maze', pygame.font.Font(None, 60), WHITE, screen, 20, 20)
        draw_text('Play', pygame.font.Font(None, 50), GREEN, screen, 20, 100)
        draw_text('Config', pygame.font.Font(None, 50), GREEN, screen, 20, 160)

        mx, my = pygame.mouse.get_pos()

        button_play = pygame.Rect(20, 100, 200, 50)
        button_config = pygame.Rect(20, 160, 200, 50)

        if button_play.collidepoint((mx, my)):
            if click:
                game = Game()
                game.run()
        if button_config.collidepoint((mx, my)):
            if click:
                config_menu()  # This will navigate to the configuration menu

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()

def draw_button(text, font, color, surface, x, y, width, height, active_color, is_active):
    rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(surface, active_color if is_active else color, rect)
    draw_text(text, font, BLACK, surface, x + 10, y + 10)
    return rect

def config_menu():
    global CELL_SIZE, MAZE_SCREEN_WIDTH, MAZE_SCREEN_HEIGHT, VISIBILITY_RATE
    running = True
    maze_size = 'Medium'  # Default selections
    enemy_count = 'Normal'

    while running:
        screen.fill(BLACK)
        draw_text('Configuration', pygame.font.Font(None, 50), WHITE, screen, 20, 20)

        # Maze Size Buttons
        small_maze_btn = draw_button('Small', pygame.font.Font(None, 40), WHITE, screen, 220, 100, 100, 40, GREEN, maze_size == 'Small')
        medium_maze_btn = draw_button('Medium', pygame.font.Font(None, 40), WHITE, screen, 330, 100, 100, 40, GREEN, maze_size == 'Medium')
        large_maze_btn = draw_button('Large', pygame.font.Font(None, 40), WHITE, screen, 440, 100, 100, 40, GREEN, maze_size == 'Large')

        # Enemies Buttons
        few_enemies_btn = draw_button('Few', pygame.font.Font(None, 40), WHITE, screen, 220, 160, 100, 40, GREEN, enemy_count == 'Few')
        normal_enemies_btn = draw_button('Normal', pygame.font.Font(None, 40), WHITE, screen, 330, 160, 100, 40, GREEN, enemy_count == 'Normal')
        many_enemies_btn = draw_button('Many', pygame.font.Font(None, 40), WHITE, screen, 440, 160, 100, 40, GREEN, enemy_count == 'Many')

        click = False
        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        if click:
            if small_maze_btn.collidepoint((mx, my)):
                maze_size = 'Small'
                MAZE_SCREEN_WIDTH, MAZE_SCREEN_HEIGHT = 400, 200
            elif medium_maze_btn.collidepoint((mx, my)):
                maze_size = 'Medium'
                MAZE_SCREEN_WIDTH, MAZE_SCREEN_HEIGHT = 600, 400
            elif large_maze_btn.collidepoint((mx, my)):
                maze_size = 'Large'
                MAZE_SCREEN_WIDTH, MAZE_SCREEN_HEIGHT = 800, 600

            if few_enemies_btn.collidepoint((mx, my)):
                enemy_count = 'Few'

            elif normal_enemies_btn.collidepoint((mx, my)):
                enemy_count = 'Normal'

            elif many_enemies_btn.collidepoint((mx, my)):
                enemy_count = 'Many'


        pygame.display.update()

if __name__ == "__main__":
    main_menu()
