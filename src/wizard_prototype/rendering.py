import curses

from wizard_prototype.game import state


class Renderer:
    def __init__(self, stdscr: curses.window):
        self.stdscr = stdscr

    def update(self, game_state: state.GameState):
        self.stdscr.clear()
        self.stdscr.addstr(
            game_state.player.position[0], game_state.player.position[1], ""
        )

        for projectile in game_state.projectiles:
            self.stdscr.addstr(projectile.position[0], projectile.position[1], "󰈸")

        if game_state.debug:
            self.stdscr.addstr(0, 0, game_state.debug)
