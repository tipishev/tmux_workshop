import curses
import time

RED = curses.COLOR_RED
GREEN = curses.COLOR_GREEN
BLUE = curses.COLOR_BLUE
YELLOW = curses.COLOR_YELLOW

def main(stdscr):
    curses.start_color()
    curses.init_pair(RED, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(GREEN, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(BLUE, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(YELLOW, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    curses.curs_set(0)
    stdscr.nodelay(1)

    battery = 100

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Habitat A", curses.color_pair(BLUE))
        stdscr.addstr(2, 0, f"Battery: {battery}%")
        stdscr.addstr(4, 0, "Press 'x' to charge", curses.color_pair(GREEN))
        stdscr.refresh()
        battery = max(battery - 1, 0)
        time.sleep(1)
        key = stdscr.getch()
        if key == ord('x'):            
            battery = 100
            stdscr.addstr(3, 0, "Battery charging...", curses.color_pair(YELLOW))
            stdscr.refresh()
            time.sleep(2)

curses.wrapper(main)