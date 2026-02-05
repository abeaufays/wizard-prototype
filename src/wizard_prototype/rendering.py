import curses

from wizard_prototype.game import state
from wizard_prototype.utils import Vec2D


class Renderer:
    def __init__(self, stdscr: curses.window):
        self.stdscr = stdscr

    def update(self, game_state: state.GameState):
        self.stdscr.clear()

        self._draw_character(game_state.player.position, "")

        for spell in game_state.spells:
            if spell.form:
                for position in spell.form.affected_tiles():
                    self._draw_character(position, spell.base.element)  # TODO

        if game_state.debug:
            self.stdscr.addstr(0, 0, game_state.debug)

    def _draw_character(self, position: Vec2D, char: str) -> None:
        if (
            0 <= position[0] < self.stdscr.getmaxyx()[0]
            and 0 <= position[1] < self.stdscr.getmaxyx()[1]
        ):
            self.stdscr.addstr(position[0], position[1], char)
