import curses

from wizard_prototype import game


class Renderer:
    def __init__(self, stdscr: curses.window):
        self.stdscr = stdscr

    def update(self, game_state: game.GameState):
        self.stdscr.clear()
        self.stdscr.addstr(
            game_state.player_position[0], game_state.player_position[1], ""
        )
