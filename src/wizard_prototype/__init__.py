import curses

from wizard_prototype.app import start_app


def main() -> None:
    curses.wrapper(start_app)
