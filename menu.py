import pygame
from button import Button
from tictacboard import Board


class Menu:
    def __init__(self):
        self.board = Board()
        self.two_player_button = pygame.image.load("images/botvsbot.png")
        self.two_player_button = pygame.transform.scale(self.two_player_button, (300, 100))
        self.player_bot_button = pygame.image.load("images/botvsbot.png")
        self.player_bot_button = pygame.transform.scale(self.player_bot_button, (300, 100))
        self.bot_bot_button = pygame.image.load("images/botvsbot.png")
        self.bot_bot_button = pygame.transform.scale(self.bot_bot_button, (300, 100))
        self.quit_button = pygame.image.load("images/playervsplayer.png")
        self.quit_button = pygame.transform.scale(self.quit_button, (300, 100))

        self.two_player_button = Button(225, 135, self.two_player_button, "Player vs Player")
        self.player_bot_button = Button(225, 220, self.player_bot_button, "Player vs Bot")
        self.bot_bot_button = Button(225, 305, self.bot_bot_button, "Bot vs Bot")
        self.quit_button = Button(225, 390, self.quit_button, "Quit")

        # Play again
        self.play_again_yes = pygame.image.load("images/botvsbot.png")
        self.play_again_yes = pygame.transform.scale(self.play_again_yes, (300, 100))
        self.play_again_no = pygame.image.load("images/playervsplayer.png")
        self.play_again_no = pygame.transform.scale(self.play_again_no, (300, 100))

        self.play_again_yes = Button(225, 200, self.play_again_yes, "Yes")
        self.play_again_no = Button(225, 280, self.play_again_no, "No")

        # Choose Sides

        self.x_button = pygame.image.load("images/botvsbot.png")
        self.x_button = pygame.transform.scale(self.x_button, (300, 100))
        self.o_button = pygame.image.load("images/playervsbot.png")
        self.o_button = pygame.transform.scale(self.o_button, (300, 100))
        self.back_button = pygame.image.load("images/playervsplayer.png")
        self.back_button = pygame.transform.scale(self.back_button, (300, 100))

        self.o_button = Button(225, 200, self.o_button, "O")
        self.x_button = Button(225, 280, self.x_button, "X")
        self.back_button = Button(225, 360, self.back_button, "Go Back")


    def draw_text(self, text, font, text_col, x, y):
        menu_text = self.board.font.render(text, True, text_col)
        self.board.screen.blit(menu_text, (x, y))

    def scoreboard(self, text, font, text_col, x, y):
        score_text = self.board.font.render(text, True, text_col)
        self.board.screen.blit(score_text, (x, y))