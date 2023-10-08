from tictacboard import Board
import pygame


class Button:
    def __init__(self, x, y, image, text_input):
        self.board = Board()
        self.image = image
        self.rect = image.get_rect(center=(x, y))
        self.text_input = text_input
        self.text = self.board.game_font.render(self.text_input, True, "black")
        self.text_rect = self.text.get_rect(center=(x, y))
        self.clicked = False

    def draw_button(self):
        action = False
        # get mouse position
        pos = pygame.mouse.get_pos()

        # check if mouse is clicked
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        # when mouse is not on pressed, change click to false
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        self.board.screen.blit(self.image, (self.rect.x, self.rect.y))
        self.board.screen.blit(self.text, self.text_rect)

        return action
