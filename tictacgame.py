import random
from collections import defaultdict
from menu import Menu

from tictacboard import Board
import pygame


class PlayervsPlayer:
    def __init__(self):
        self.board = Board()
        self.menu = Menu()
        self.player = None
        self.winner = None
        self.taking_move = True
        self.choice = None
        self.x_score = 0
        self.o_score = 0

    def change_player(self):
        self.player = "O" if self.player == "X" else "X"

    def move_player(self, pos):
        try:
            x, y = pos[0] // self.board.cell_size, pos[1] // self.board.cell_size
            if self.board.table[x][y] == "-":
                self.board.table[x][y] = self.player
                self.draw(x, y, self.player)
                self.is_game_over()
                self.change_player()
        except:
            print("Please click inside the table only")

    def draw(self, x, y, player):
        if self.player == "X":
            img = pygame.image.load("images/x.png")
        elif self.player == "O":
            img = pygame.image.load("images/o.png")

        # Define a margin value to add space around the image
        margin = 20
        img = pygame.transform.scale(img, (self.board.cell_size - 2 * margin, self.board.cell_size - 2 * margin))

        # Calculate the new position with margin
        img_x = x * self.board.cell_size + margin
        img_y = y * self.board.cell_size + margin

        self.board.screen.blit(img,
                               (img_x, img_y, self.board.cell_size - 2 * margin, self.board.cell_size - 2 * margin))

    def message(self):
        if self.winner is not None and self.winner == "X":
            self.board.screen.fill(self.board.game_over_bg_color_x, (100, 455, 248, 55))
            msg = self.board.font.render(f"{self.winner} WINS !! ", True, self.board.game_over_color_x)
            self.board.screen.blit(msg, (175, 458))
        elif self.winner is not None and self.winner == "O":
            self.board.screen.fill(self.board.game_over_bg_color_o, (100, 455, 248, 55))
            msg = self.board.font.render(f"{self.winner} WINS !! ", True, self.board.game_over_color_o)
            self.board.screen.blit(msg, (175, 458))
        elif not self.taking_move:
            self.board.screen.fill(self.board.draw, (100, 455, 248, 55))
            msg = self.board.font.render("DRAW !!", True, self.board.game_over_color_o)
            self.board.screen.blit(msg, (180, 458))
        else:
            self.board.screen.fill(self.board.scoreboard_bg, (100, 455, 258, 55))
            msg = self.board.font.render(f"{self.player} Turn", True, self.board.scoreboard_color)
            self.board.screen.blit(msg, (190, 458))

    def scoreboard(self):
        self.board.screen.fill(self.board.scoreboard_bg, (0, 455, 108, 55))
        msg = self.board.score_font.render(f"X : {self.x_score}", True, self.board.scoreboard_color)
        self.board.screen.blit(msg, (25, 465))
        self.board.screen.fill(self.board.scoreboard_bg, (350, 455, 108, 55))
        msg = self.board.score_font.render(f"O : {self.o_score}", True, self.board.scoreboard_color)
        self.board.screen.blit(msg, (370, 465))

    def add_score(self):
        if self.winner == "X":
            self.x_score += 1
            self.scoreboard()
        elif self.winner == "O":
            self.o_score += 1
            self.scoreboard()
        else:
            self.x_score = self.x_score
            self.o_score = self.o_score
            self.scoreboard()

    def is_game_over(self):
        # Vertical Check
        for x_index in range(3):
            win = True
            pattern_list = []
            for y_index in range(3):
                if self.board.table[x_index][y_index] != self.player:
                    win = False
                    break
                else:
                    pattern_list.append((x_index, y_index))

            if win:
                self.pattern_check(pattern_list[0], pattern_list[-1], 'ver')
                self.winner = self.player
                self.add_score()
                self.taking_move = False
                self.message()

        # Horizontal Check
        for y_index in range(3):
            win = True
            pattern_list = []
            for x_index in range(3):
                if self.board.table[x_index][y_index] != self.player:
                    win = False
                    break
                else:
                    pattern_list.append((x_index, y_index))

            if win:
                self.pattern_check(pattern_list[0], pattern_list[-1], 'hor')
                self.winner = self.player
                self.add_score()
                self.taking_move = False
                self.message()

        # right diagonal check
        if all(self.board.table[i][i] == self.player for i in range(3)):
            self.pattern_check((0, 0), (2, 2), 'right-diag')
            self.winner = self.player
            self.add_score()
            self.taking_move = False
            self.message()

        # left diagonal check
        if all(self.board.table[i][2 - i] == self.player for i in range(3)):
            self.pattern_check((0, 2), (2, 0), 'left-diag')
            self.winner = self.player
            self.add_score()
            self.taking_move = False
            self.message()

        # Check empty Cells
        blank_cells = 0
        for row in self.board.table:
            for col in row:
                if col == "-":
                    blank_cells += 1
        if blank_cells == 0:
            self.taking_move = False
            self.add_score()
            self.message()

    def pattern_check(self, start_point, end_point, line_type):
        """Checks the winner"""
        mid_val = self.board.cell_size // 2

        # Checks Vertical Pattern
        if line_type == "ver":
            start_x, start_y = start_point[0] * self.board.cell_size + mid_val, self.board.table_space
            end_x, end_y = end_point[0] * self.board.cell_size + mid_val, self.board.table_size - self.board.table_space

        # Checks Horizontal Pattern
        elif line_type == "hor":
            start_x, start_y = self.board.table_space, start_point[-1] * self.board.cell_size + mid_val
            end_x, end_y = self.board.table_size - self.board.table_space, end_point[
                -1] * self.board.cell_size + mid_val

        # Checks Right Diagonal
        elif line_type == "left-diag":
            start_x, start_y = self.board.table_size - self.board.table_space, self.board.table_space
            end_x, end_y = self.board.table_space, self.board.table_size - self.board.table_space

        # Checks Left Diagonal
        elif line_type == "right-diag":
            start_x, start_y = self.board.table_space, self.board.table_space
            end_x, end_y = self.board.table_size - self.board.table_space, self.board.table_size - self.board.table_space

        if self.player == "X":
            line_check = pygame.draw.line(self.board.screen, self.board.line_color_x, [start_x, start_y],
                                          [end_x, end_y], 8)
        else:
            line_check = pygame.draw.line(self.board.screen, self.board.line_color_o, [start_x, start_y],
                                          [end_x, end_y], 8)

    def reset_player_player(self):
        self.board.reset_table()
        self.winner = None
        self.taking_move = True
        self.player = self.choice


class PlayervsBot(PlayervsPlayer):
    def __init__(self):
        super().__init__()
        self.player_turn = True
        self.bot_delay = 3000
        self.bot_timer = pygame.time.set_timer(pygame.USEREVENT, self.bot_delay)
        self.original_player = None
        self.bot = None
        self.choice = None
        self.bot_choice = None
        self.player = None

    def player_move(self, pos):
        try:
            x, y = pos[0] // self.board.cell_size, pos[1] // self.board.cell_size
            if self.board.table[x][y] == "-" and self.player_turn:
                self.board.table[x][y] = self.player
                self.draw(x, y, self.player)
                self.is_game_over()
                self.change_player()
                self.player_turn = False
        except:
            print("Please click inside the table only")

    def bot_move(self):

        winning_play = self._get_possible_play(play_type='offensive')
        if winning_play:
            x, y = winning_play
            if self.board.table[x][y] == "-":
                self.board.table[x][y] = self.bot
                self.draw(x, y, self.bot)
                self.is_game_over()
                self.change_player()
                self.player_turn = True
                return

        blocking_play = self._get_possible_play(play_type='defensive')
        if blocking_play:
            x, y = blocking_play
            if self.board.table[x][y] == "-":
                self.board.table[x][y] = self.bot
                self.draw(x, y, self.bot)
                self.is_game_over()
                self.change_player()
                self.player_turn = True
                return

        completion_play = self._get_possible_play(play_type='completion')
        if completion_play:
            x, y = completion_play
            if self.board.table[x][y] == "-":
                self.board.table[x][y] = self.bot
                self.draw(x, y, self.bot)
                self.is_game_over()
                self.change_player()
                self.player_turn = True
                return

        random_play = self._get_possible_play(play_type='random')
        if random_play:
            x, y = random_play
            self.board.table[x][y] = self.bot
            self.draw(x, y, self.bot)
            self.is_game_over()
            self.change_player()
            self.player_turn = True
            return

    def _get_possible_play(self, play_type='offensive'):
        game = self.board.table
        sought_symbol = self.bot

        if play_type == 'random':
            empty_cells = [(x, y) for x in range(3) for y in range(3) if self.board.table[x][y] == "-"]
            random_pos = random.choice(empty_cells)
            x, y = random_pos[0], random_pos[1]
            return x, y

        if play_type == 'defensive':
            # Determine the opponent's symbol by iterating through the cells
            for x in range(3):
                for y in range(3):
                    if game[x][y] != '-' and game[x][y] != self.bot:
                        # Change the sought symbol to the opponent's symbol
                        sought_symbol = game[x][y]
                        break

        for line in self.board.lines:
            line_state = defaultdict(int)
            empty_positions = []

            for pos in line.indices:
                x, y = pos // 3, pos % 3
                symbol = game[x][y]

                if symbol == '-':
                    empty_positions.append((x, y))
                line_state[symbol] += 1
            if play_type == 'completion':
                if line_state[sought_symbol] == 1 and line_state['-'] == 2:
                    empty_pos = random.choice(empty_positions)
                    return empty_pos
            else:
                if line_state[sought_symbol] == 2 and line_state['-'] == 1:
                    empty_pos = empty_positions[0]
                    return empty_pos
        return None

    def reset_player_player(self):
        super().reset_player_player()
        self.player_turn = True
        self.bot_delay = 3000
        self.original_player = self.choice
        self.bot = self.bot_choice
        self.player = self.choice


class BotvsBot(PlayervsPlayer):
    def __init__(self):
        super().__init__()
        self.taking_move = True
        self.bot_a_start = True
        self.bot_b_start = False
        self.bot_a_delay = 3000
        self.bot_b_delay = 2000
        self.last_bot_move_time = pygame.time.get_ticks()
        self.bot_a = "X"
        self.bot_b = "O"
        self.player = "X"

    def bot_a_move(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_bot_move_time >= self.bot_a_delay:

            winning_play = self._get_possible_play_a(play_type='offensive')
            if winning_play:
                x, y = winning_play
                if self.board.table[x][y] == "-" and self.bot_a_start:
                    self.board.table[x][y] = self.bot_a
                    self.draw(x, y, self.bot_a)
                    self.is_game_over()
                    self.change_player()
                    self.bot_a_start = False
                    self.bot_b_start = True
                    self.last_bot_move_time = current_time
                    return

            blocking_play = self._get_possible_play_a(play_type='defensive')
            if blocking_play:
                x, y = blocking_play
                if self.board.table[x][y] == "-" and self.bot_a_start:
                    self.board.table[x][y] = self.bot_a
                    self.draw(x, y, self.bot_a)
                    self.is_game_over()
                    self.change_player()
                    self.bot_a_start = False
                    self.bot_b_start = True
                    self.last_bot_move_time = current_time
                    return

            completion_play = self._get_possible_play_a(play_type='completion')
            if completion_play:
                x, y = completion_play
                if self.board.table[x][y] == "-" and self.bot_a_start:
                    self.board.table[x][y] = self.bot_a
                    self.draw(x, y, self.bot_a)
                    self.is_game_over()
                    self.change_player()
                    self.bot_a_start = False
                    self.bot_b_start = True
                    self.last_bot_move_time = current_time
                    return

            random_play = self._get_possible_play_a(play_type='random')
            if random_play:
                x, y = random_play
                self.board.table[x][y] = self.bot_a
                self.draw(x, y, self.bot_a)
                self.is_game_over()
                self.change_player()
                self.bot_a_start = False
                self.bot_b_start = True
                self.last_bot_move_time = current_time
                return

    def _get_possible_play_a(self, play_type='offensive'):
        game = self.board.table
        sought_symbol = self.bot_a

        if play_type == 'random':
            empty_cells = [(x, y) for x in range(3) for y in range(3) if self.board.table[x][y] == "-"]
            random_pos = random.choice(empty_cells)
            x, y = random_pos[0], random_pos[1]
            return x, y

        if play_type == 'defensive':
            # Determine the opponent's symbol by iterating through the cells
            for x in range(3):
                for y in range(3):
                    if game[x][y] != '-' and game[x][y] != self.bot_a:
                        # Change the sought symbol to the opponent's symbol
                        sought_symbol = game[x][y]
                        break

        for line in self.board.lines:
            line_state = defaultdict(int)
            empty_positions = []

            for pos in line.indices:
                x, y = pos // 3, pos % 3
                symbol = game[x][y]

                if symbol == '-':
                    empty_positions.append((x, y))
                line_state[symbol] += 1
            if play_type == 'completion':
                if line_state[sought_symbol] == 1 and line_state['-'] == 2:
                    empty_pos = random.choice(empty_positions)
                    return empty_pos
            else:
                if line_state[sought_symbol] == 2 and line_state['-'] == 1:
                    empty_pos = empty_positions[0]
                    return empty_pos
        return None

    def bot_b_move(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_bot_move_time >= self.bot_b_delay:
            winning_play = self._get_possible_play_b(play_type='offensive')
            if winning_play:
                x, y = winning_play
                if self.board.table[x][y] == "-" and self.bot_b_start:
                    self.board.table[x][y] = self.bot_b
                    self.draw(x, y, self.bot_b)
                    self.is_game_over()
                    self.change_player()
                    self.bot_b_start = False
                    self.bot_a_start = True
                    self.last_bot_move_time = current_time
                    return

            blocking_play = self._get_possible_play_b(play_type='defensive')
            if blocking_play:
                x, y = blocking_play
                if self.board.table[x][y] == "-" and self.bot_b_start:
                    self.board.table[x][y] = self.bot_b
                    self.draw(x, y, self.bot_b)
                    self.is_game_over()
                    self.change_player()
                    self.bot_b_start = False
                    self.bot_a_start = True
                    self.last_bot_move_time = current_time
                    return

            completion_play = self._get_possible_play_b(play_type='completion')
            if completion_play:
                x, y = completion_play
                if self.board.table[x][y] == "-" and self.bot_b_start:
                    self.board.table[x][y] = self.bot_b
                    self.draw(x, y, self.bot_b)
                    self.is_game_over()
                    self.change_player()
                    self.bot_b_start = False
                    self.bot_a_start = True
                    self.last_bot_move_time = current_time
                    return

            random_play = self._get_possible_play_b(play_type='random')
            if random_play:
                x, y = random_play
                self.board.table[x][y] = self.bot_b
                self.draw(x, y, self.bot_b)
                self.is_game_over()
                self.change_player()
                self.bot_b_start = False
                self.bot_a_start = True
                self.last_bot_move_time = current_time
                return

    def _get_possible_play_b(self, play_type='offensive'):
        game = self.board.table
        sought_symbol = self.bot_b

        if play_type == 'random':
            empty_cells = [(x, y) for x in range(3) for y in range(3) if self.board.table[x][y] == "-"]
            random_pos = random.choice(empty_cells)
            x, y = random_pos[0], random_pos[1]
            return x, y

        if play_type == 'defensive':
            # Determine the opponent's symbol by iterating through the cells
            for x in range(3):
                for y in range(3):
                    if game[x][y] != '-' and game[x][y] != self.bot_b:
                        # Change the sought symbol to the opponent's symbol
                        sought_symbol = game[x][y]
                        break

        for line in self.board.lines:
            line_state = defaultdict(int)
            empty_positions = []

            for pos in line.indices:
                x, y = pos // 3, pos % 3
                symbol = game[x][y]

                if symbol == '-':
                    empty_positions.append((x, y))
                line_state[symbol] += 1
            if play_type == 'completion':
                if line_state[sought_symbol] == 1 and line_state['-'] == 2:
                    empty_pos = random.choice(empty_positions)
                    return empty_pos
            else:
                if line_state[sought_symbol] == 2 and line_state['-'] == 1:
                    empty_pos = empty_positions[0]
                    return empty_pos
        return None

    def reset_player_player(self):
        super().reset_player_player()
        self.taking_move = True
        self.bot_a_start = True
        self.bot_b_start = False
        self.bot_a = "X"
        self.bot_b = "O"
        self.player = "X"
