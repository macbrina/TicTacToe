import pygame
from collections import namedtuple
Line = namedtuple('Line', 'name indices')
window_size = (450, 500)
pygame.display.set_caption("Tic Tac Toe")


class Board:
    def __init__(self):
        # Every possible winning condition is represented by a Line.
        self.lines = (
            Line('row A', (0, 1, 2)),
            Line('row B', (3, 4, 5)),
            Line('row C', (6, 7, 8)),
            Line('column 1', (0, 3, 6)),
            Line('column 2', (1, 4, 7)),
            Line('column 3', (2, 5, 8)),
            Line('first diagonal', (0, 4, 8)),
            Line('second diagonal', (2, 4, 6))
        )
        self.screen = pygame.display.set_mode(window_size)
        self.table_size = window_size[0]
        self.cell_size = self.table_size // 3
        self.table_space = 20
        self.table = []
        for col in range(3):
            self.table.append([])
            for row in range(3):
                self.table[col].append("-")

        self.background_color = (245, 245, 220)
        self.menu_state = "main"
        self.menu_color = (255, 207, 157)
        self.line_color_x = (255, 255, 255)
        self.line_color_o = (0, 0, 0)
        self.instruction_color = (17, 53, 165)
        self.draw = (255, 207, 157)
        self.game_over_bg_color_x = (0, 66, 37)
        self.game_over_color_x = (255, 255, 255)
        self.game_over_bg_color_o = (255, 176, 0)
        self.game_over_color_o = (0, 0, 0)
        self.scoreboard_bg = (255, 207, 157)
        self.scoreboard_color = (0, 0, 0)
        self.table_color = (50, 50, 50)
        self.score_font = pygame.font.SysFont("ebrima", 40)
        self.font = pygame.font.SysFont("impact", 30)
        self.game_font = pygame.font.SysFont("javanesetext", 30)
        self.FPS = pygame.time.Clock()

    def table_line(self):
        tb_space = (self.table_space, self.table_size - self.table_space)
        cell_space = (self.cell_size, self.cell_size * 2)
        a1 = pygame.draw.line(self.screen, self.table_color, [tb_space[0], cell_space[0]], [tb_space[1], cell_space[0]],
                              8)
        b1 = pygame.draw.line(self.screen, self.table_color, [cell_space[0], tb_space[0]], [cell_space[0], tb_space[1]],
                              8)
        a2 = pygame.draw.line(self.screen, self.table_color, [tb_space[0], cell_space[1]], [tb_space[1], cell_space[1]],
                              8)
        b2 = pygame.draw.line(self.screen, self.table_color, [cell_space[1], tb_space[0]], [cell_space[1], tb_space[1]],
                              8)

    def reset_table(self):
        self.table = []
        for col in range(3):
            self.table.append([])
            for row in range(3):
                self.table[col].append("-")
