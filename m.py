import curses

def main(stdscr):
    # Initialize curses
    curses.start_color()
    curses.use_default_colors()

    # Use extended colors if available
    for i in range(0, curses.COLORS):
        curses.init_pair(i + 1, i, -1)

    # Print some text with different colors
    for i in range(0, curses.COLORS):
        stdscr.addstr(str(i), curses.color_pair(i))

    stdscr.refresh()
    stdscr.getch()

curses.wrapper(main)