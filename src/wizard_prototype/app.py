import curses

from wizard_prototype import rendering
from wizard_prototype.game import state


def start_app(stdscr: curses.window):
    App(stdscr)


class App:
    def __init__(self, stdscr: curses.window):
        stdscr.clear()
        self.renderer = rendering.Renderer(stdscr)
        self.game_state = state.GameState()
        curses.noecho()
        curses.curs_set(False)

        self.renderer.update(self.game_state)
        while True:
            cmd = stdscr.getkey()
            if cmd == "q":
                break
            self.main_loop(cmd)

    def main_loop(self, cmd: str):
        self.game_state.update(cmd)
        self.renderer.update(self.game_state)
