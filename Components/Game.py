import pygame
from Config import *
from Maze import Maze
from Player import Player
from EldritchSpawn import EldritchSpawn
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
        small_maze_btn = draw_button('Small', pygame.font.Font(None, 40), WHITE, screen, 220, 100, 100, 40, GREEN,
                                     maze_size == 'Small')
        medium_maze_btn = draw_button('Medium', pygame.font.Font(None, 40), WHITE, screen, 330, 100, 100, 40, GREEN,
                                      maze_size == 'Medium')
        large_maze_btn = draw_button('Large', pygame.font.Font(None, 40), WHITE, screen, 440, 100, 100, 40, GREEN,
                                     maze_size == 'Large')

        # Enemies Buttons
        few_enemies_btn = draw_button('Few', pygame.font.Font(None, 40), WHITE, screen, 220, 160, 100, 40, GREEN,
                                      enemy_count == 'Few')
        normal_enemies_btn = draw_button('Normal', pygame.font.Font(None, 40), WHITE, screen, 330, 160, 100, 40, GREEN,
                                         enemy_count == 'Normal')
        many_enemies_btn = draw_button('Many', pygame.font.Font(None, 40), WHITE, screen, 440, 160, 100, 40, GREEN,
                                       enemy_count == 'Many')

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
    pygame.init()
    main_menu()
