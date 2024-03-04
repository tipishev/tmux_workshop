'''
this script provides a curses-based client to query the state of the rover
sample request: GET http://localhost:5000/rovers?name=Chip
interface is drawn similar to the habitat client.

The base name is extracted from args and used to query the state of the base. The state is then displayed on the screen.
'''

import curses
import requests
import time
import sys

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

    rover_name = sys.argv[1]
    while True:
        try:
            response = requests.get(f"http://localhost:5000/rover?name={rover_name}")
            rover = response.json()
        except requests.exceptions.ConnectionError:
            # clear screen and display error message
            stdscr.clear()
            stdscr.addstr(0, 0, f"Telemetry to {rover_name} is lost", curses.color_pair(RED))
        else:
            stdscr.clear()
            stdscr.addstr(0, 0, f"{rover_name}", curses.color_pair(BLUE))
            stdscr.addstr(1, 0, f"{display_cargo(rover['cargo'])}")
            stdscr.addstr(2, 0, f"location: {display_location(rover['location'])}")
            stdscr.addstr(3, 0, f"state: {rover['state']}")
        stdscr.refresh()
        time.sleep(1)

def display_cargo(cargo: dict):
    # filter for non-zero cargo
    cargo = {k: v for k, v in cargo.items() if v > 0}
    emoji_lookup = {"energy": "🔋", "water": "💧"}
    return ' '.join([f"{emoji_lookup[k]} {v}" for k, v in cargo.items()])

def display_location(index: int):
    if index == 1:
        return "1 (ICE)"
    elif index == 10:
        return "10 (SOL)"
    else:
        return str(index)

curses.wrapper(main)