import sys

import pyautogui as pg
import pydirectinput as pdi
import win32api
import win32con
from pynput.keyboard import Listener, Key

import time

from keys import VK_CODE

# Chapters:
# 1. Prologue
# 2. Inside the Wall
# 3. Dead City
# 4. The Flat
# 5. Slums
# 6. The Slums - Part 2
# 7. Dead End
# 8. Sewers
# 9. Antvillage
# 10. Midtown
# 11. Jail
# 12. Control Room

flag = False

for t in range(3, 0, -1):
    print(f"Starting in {t}", end="\r")
    time.sleep(1)
print("Starting")

# start
screenWidth, screenHeight = pg.size()


# utilities
def wait(duration):
    if duration < 1:
        return time.sleep(duration)

    # account for error
    duration = duration * 0.97

    while not flag:
        time.sleep(0.01)
        duration -= 0.01
        if duration <= 0:
            break


def check_press(key):
    if key == Key.esc:
        print("Exiting")
        global flag
        flag = True
        sys.exit(0)


def start():
    pdi.leftClick(screenWidth // 2, int(screenHeight * .8))
    wait(0.1)
    pdi.leftClick(screenWidth // 2, screenHeight // 2)
    wait(0.1)
    pdi.leftClick(screenWidth // 2, int(screenHeight * .8))
    pdi.leftClick(int(screenWidth * .56), int(screenHeight * .55))
    wait(0.1)
    pdi.leftClick(screenWidth // 2, screenHeight // 2)
    wait(0.1)
    pdi.moveTo(screenWidth // 2, int(screenHeight * .7))


def wait_play():
    while pg.pixel(screenWidth // 2, int(screenHeight * .9)) == (0, 0, 0) and not flag:
        time.sleep(0.01)


def press_down(_key):
    """
    one press, one release.
    accepts as many arguments as you want. e.g., press("left_arrow", "a","b").
    """
    win32api.keybd_event(VK_CODE[_key], 0, 0, 0)


def press_up(_key):
    """
    one press, one release.
    :param _key:
    :return:
    """
    win32api.keybd_event(VK_CODE[_key], 0, win32con.KEYEVENTF_KEYUP, 0)


if __name__ == '__main__':
    try:
        listener = Listener(on_press=check_press)
        listener.start()

        # start()
        pdi.press('enter')
        wait(2)

        files = [
            # "prologue.txt",
            # "inside_walls.txt",
            "out.txt"
        ]
        for file in files:
            file = "captures/" + file

            lines = []
            prev_line = None
            with open(file, "r") as f:
                for line in f:
                    if line.startswith("#"):
                        continue

                    if prev_line is None:
                        prev_line = line.split(" ")
                        continue

                    line = line.split(" ")

                    now_time = float(line[2])
                    prev_time = float(prev_line[2])

                    dur = now_time - prev_time

                    lines.append([prev_line[0], prev_line[1], dur])
                    print(lines[-1])

                    prev_line = line

                    if flag:
                        break

            wait_play()
            print(f'Playing `{file.split(".")[0].replace("_", " ")}`')

            for line in lines:
                if flag:
                    break

                if line[0] == "/\\":
                    press_up(line[1])
                elif line[0] == "\\/":
                    press_down(line[1])
                else:
                    print(f"Invalid line: {line}")

                time.sleep(line[2])
    finally:
        # release all keys
        for k in [
            "w", "a", "s", "d",
            "space", "shift", "ctrl", "alt",
            "e", "q", "r", "f",
            "tab"
        ]:
            pg.keyUp(k)
