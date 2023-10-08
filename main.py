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
    while game_running:
        while board.menu_state == "main":
            board.screen.fill(board.menu_color)
            menu.draw_text("MENU", board.font, "black", 190, 40)

            menu.two_player_button.draw_button()
            menu.player_bot_button.draw_button()
            menu.bot_bot_button.draw_button()
            menu.quit_button.draw_button()

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    board.menu_state = "exit"

                two_player_clicked = menu.two_player_button.draw_button()
                player_bot_clicked = menu.player_bot_button.draw_button()
                bot_bot_clicked = menu.bot_bot_button.draw_button()
                quit_clicked = menu.quit_button.draw_button()

                # Check if any button was clicked
                if two_player_clicked:
                    board.menu_state = "two-player"
                    board.screen.fill(board.background_color)
                    board.table_line()
                elif player_bot_clicked:
                    board.menu_state = "bot-player"
                    board.screen.fill(board.background_color)
                    board.table_line()
                elif bot_bot_clicked:
                    board.menu_state = "bot-bot"
                    board.screen.fill(board.background_color)
                    board.table_line()
                elif quit_clicked:
                    game_running = False

            pygame.display.update()
            board.FPS.tick(60)
            if not game_running:
                break

        while board.menu_state == "two-player":

            if not two_player.taking_move:
                pygame.time.wait(3000)
                board.menu_state = "game-over"

            two_player.message()
            two_player.scoreboard()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_running = False

                mouse_down = pygame.mouse.get_pressed()

                if event.type == pygame.MOUSEBUTTONDOWN and mouse_down[0]:
                    if two_player.taking_move:
                        two_player.move_player(event.pos)

            pygame.display.update()
            board.FPS.tick(60)
            if not game_running:
                break

        while board.menu_state == "bot-player":
            if not bot_player.taking_move:
                pygame.time.wait(3000)
                board.menu_state = "game-over"

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

            pygame.display.update()
            board.FPS.tick(60)
            if not game_running:
                break


        while board.menu_state == "bot-bot":
            if not bot_bot.taking_move:
                pygame.time.wait(3000)
                board.menu_state = "game-over"

            bot_bot.message()
            bot_bot.scoreboard()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_running = False

            if bot_bot.taking_move and not bot_bot.bot_b_start and bot_bot.winner is None:
                bot_bot.bot_a_move()
            elif bot_bot.taking_move and not bot_bot.bot_a_start and bot_bot.winner is None:
                bot_bot.bot_b_move()


            pygame.display.update()
            board.FPS.tick(60)
            if not game_running:
                break

        while board.menu_state == "game-over":
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
                    board.menu_state = "main"
                    two_player.reset_player_player()
                    bot_player.reset_player_player()
                    bot_bot.reset_player_player()
                elif no_play_again:
                    game_running = False
            pygame.display.flip()
            board.FPS.tick(60)
            if not game_running:
                break

    pygame.quit()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Game aborted by user.')
