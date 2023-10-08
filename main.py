import pygame
import pygame.font
from tictacgame import PlayervsPlayer, PlayervsBot, BotvsBot
from tictacboard import Board
from menu import Menu

pygame.init()
pygame.font.init()

board = Board()
two_player = PlayervsPlayer()
bot_player = PlayervsBot()
bot_bot = BotvsBot()
menu = Menu()


def main():
    game_running = True
    previous_button = None
    current_state = "main"

    while game_running:

        if current_state == "main":
            board.screen.fill(board.menu_color)
            menu.draw_text("MENU", board.font, "black", 190, 40)
            menu.two_player_button.draw_button()
            menu.player_bot_button.draw_button()
            menu.bot_bot_button.draw_button()
            menu.quit_button.draw_button()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_running = False

                two_player_clicked = menu.two_player_button.draw_button()
                player_bot_clicked = menu.player_bot_button.draw_button()
                bot_bot_clicked = menu.bot_bot_button.draw_button()
                quit_clicked = menu.quit_button.draw_button()

                if two_player_clicked:
                    previous_button = "two-player"
                    if two_player.player is None:
                        current_state = "choose-side"
                    else:
                        current_state = "two-player"
                        board.screen.fill(board.background_color)
                        board.table_line()
                elif player_bot_clicked:
                    previous_button = "bot-player"
                    if bot_player.player is None:
                        current_state = "choose-side"
                    else:
                        current_state = "bot-player"
                        board.screen.fill(board.background_color)
                        board.table_line()
                elif bot_bot_clicked:
                    previous_button = "bot-bot"
                    current_state = "bot-bot"
                    board.screen.fill(board.background_color)
                    board.table_line()
                elif quit_clicked:
                    game_running = False

        if current_state == "choose-side":
            if two_player.player is None or bot_player.player is None:
                board.screen.fill(board.menu_color)
                menu.x_button.draw_button()
                menu.o_button.draw_button()
                menu.back_button.draw_button()
                board.screen.fill(board.game_over_bg_color_x, (100, 105, 248, 45))
                msg = board.game_font.render(f"Choose your side", True, board.game_over_color_x)
                board.screen.blit(msg, (140, 115))

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game_running = False

                    x_button = menu.x_button.draw_button()
                    o_button = menu.o_button.draw_button()
                    back_button = menu.back_button.draw_button()
                    if previous_button == "two-player":
                        if x_button:
                            two_player.player = "X"
                            two_player.choice = "X"
                            current_state = "two-player"
                            board.screen.fill(board.background_color)
                            board.table_line()
                        elif o_button:
                            two_player.player = "O"
                            two_player.choice = "O"
                            current_state = "two-player"
                            board.screen.fill(board.background_color)
                            board.table_line()
                        elif back_button:
                            current_state = "main"
                    elif previous_button == "bot-player":
                        if x_button:
                            bot_player.player = "X"
                            bot_player.original_player = "X"
                            bot_player.choice = "X"
                            bot_player.bot_choice = "O"
                            bot_player.bot = "O"
                            current_state = "bot-player"
                            board.screen.fill(board.background_color)
                            board.table_line()
                        elif o_button:
                            bot_player.player = "O"
                            bot_player.original_player = "O"
                            bot_player.choice = "O"
                            bot_player.bot = "X"
                            bot_player.bot_choice = "X"
                            current_state = "bot-player"
                            board.screen.fill(board.background_color)
                            board.table_line()
                        elif back_button:
                            current_state = "main"

        if current_state == "two-player":
            if not two_player.taking_move:
                pygame.time.wait(3000)
                current_state = "game-over"

            two_player.message()
            two_player.scoreboard()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_running = False

                mouse_down = pygame.mouse.get_pressed()

                if event.type == pygame.MOUSEBUTTONDOWN and mouse_down[0]:
                    if two_player.taking_move:
                        two_player.move_player(event.pos)

        if current_state == "bot-player":
            if not bot_player.taking_move:
                pygame.time.wait(3000)
                current_state = "game-over"

            bot_player.message()
            bot_player.scoreboard()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_running = False

                if event.type == pygame.USEREVENT:
                    if bot_player.taking_move and not bot_player.player_turn and bot_player.winner is None:
                        bot_player.bot_move()

                mouse_down = pygame.mouse.get_pressed()

                if event.type == pygame.MOUSEBUTTONDOWN and mouse_down[0]:
                    if bot_player.taking_move and bot_player.player_turn:
                        bot_player.player_move(event.pos)

        if current_state == "bot-bot":
            if not bot_bot.taking_move:
                pygame.time.wait(3000)
                current_state = "game-over"

            bot_bot.message()
            bot_bot.scoreboard()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_running = False

            if bot_bot.taking_move and not bot_bot.bot_b_start and bot_bot.winner is None:
                bot_bot.bot_a_move()
            elif bot_bot.taking_move and not bot_bot.bot_a_start and bot_bot.winner is None:
                bot_bot.bot_b_move()

        if current_state == "game-over":
            board.screen.fill(board.menu_color)
            menu.draw_text("PLAY AGAIN?", board.font, "black", 160, 100)

            menu.play_again_yes.draw_button()
            menu.play_again_no.draw_button()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_running = False

                yes_play_again = menu.play_again_yes.draw_button()
                no_play_again = menu.play_again_no.draw_button()

                if yes_play_again:
                    current_state = "main"
                    two_player.reset_player_player()
                    bot_player.reset_player_player()
                    bot_bot.reset_player_player()
                elif no_play_again:
                    game_running = False

        pygame.display.flip()
        board.FPS.tick(60)

    pygame.quit()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Game aborted by the user.')
