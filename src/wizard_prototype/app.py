import curses


def start_app(stdscr: curses.window):
    stdscr.clear()

    curses.noecho()

    stdscr.box(0, 0)

    while True:
        cmd = stdscr.getkey()
        if cmd == "q":
            break
        main_loop(stdscr, cmd)


def main_loop(stdscr: curses.window, cmd: str):
    stdscr.addstr(10, 10, cmd)
