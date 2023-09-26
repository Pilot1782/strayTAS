import sys
import time

import pyautogui as pg
import pydirectinput as pdi
import win32api
import win32con

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


def check_press(_key):
    from pynput.keyboard import Key
    if _key == Key.esc:
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
        if "--sub" not in sys.argv:
            from pynput.keyboard import Listener
            listener = Listener(on_press=check_press)
            listener.start()

        # start()
        pdi.press('enter')
        wait(2)

        files = [
            # "prologue.txt",
            # "inside_walls.txt"
            "out.txt"
        ]
        for file in files:
            file = "captures/" + file

            lines: list[tuple[tuple, float]] = []
            prev_line = None
            with open(file, "r") as f:
                for line in f:
                    if line.startswith("#"):
                        continue

                    line = line.split(" ")

                    if prev_line is None:
                        prev_line = line
                        continue

                    now_time = float(line[2])
                    prev_time = float(prev_line[2])

                    dur = float(now_time - prev_time)

                    key = int(line[1])
                    prev_key = int(prev_line[1])

                    down = (prev_key, 0, 0, 0)
                    up = (prev_key, 0, win32con.KEYEVENTF_KEYUP, 0)

                    if prev_line[0] == "/\\":
                        lines.append((up, dur))
                    else:
                        lines.append((down, dur))
                    print(lines[-1], prev_line, f"Up: {lines[-1][0][2] == 2}")

                    prev_line = line

                    if flag:
                        break

                # write the final line
                key = int(prev_line[1])
                lines.append(((key, 0, win32con.KEYEVENTF_KEYUP, 0), 0))

            wait_play()
            print(f'Playing `{file.split(".")[0].replace("_", " ")}`')

            for line in lines:
                if flag:
                    break

                win32api.keybd_event(*line[0])

                time.sleep(line[1])
    finally:
        # release all keys
        for k in [
            "w", "a", "s", "d",
            "space", "ctrl", "alt",
            "e", "q", "r", "f",
            "tab", "esc",
            "1", "2",
            "shift", "left_shift", "right_shift",
        ]:
            press_up(k)

            """
            """
