import pickle
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
print(f"Main screen size: {screenWidth}x{screenHeight}")


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

    :param _key: the name of the key to press
    :return: None
    """
    win32api.keybd_event(VK_CODE[_key], 0, 0, 0)


def press_up(_key):
    """
    one press, one release.
    :param _key: the name of the key to release
    :return: None
    """
    win32api.keybd_event(VK_CODE[_key], 0, win32con.KEYEVENTF_KEYUP, 0)


def parse_line(_event: tuple[int, float, int, int], duration: float) -> list:
    """
    :param duration: the duration of the event
    :param _event: the line to parse
    :return: the key to press, the duration to press it for
    """
    if _event[0] == 0x02:
        print(f"Moving mouse by {_event[2]} and {_event[3]}")
        # mouse movement
        return [
            False,
            (_event[2], _event[3]),
            duration,
        ]
    elif _event[0] == 0x01:
        print(f"Releasing key {_event[2]}")
        # key release
        return [
            True,
            (int(_event[2]), 0, win32con.KEYEVENTF_KEYUP, 0),
            duration
        ]
    elif _event[0] == 0x00:
        print(f"Pressing key {_event[2]}")
        # key press
        return [
            True,
            (int(_event[2]), 0, 0, 0),
            duration
        ]


if __name__ == '__main__':
    try:
        files = [
            "out.pkl"
        ]

        # argument parsing
        if "--sub" not in sys.argv:
            from pynput.keyboard import Listener
            listener = Listener(on_press=check_press)
            listener.start()
        elif "--play" in sys.argv[1]:
            files = [
                str(sys.argv[2:])
            ]
        elif len(sys.argv) > 1:
            print("Unknown argument")

        # start the game
        # start()
        pdi.leftClick()
        wait(0.5)

        for file in files:
            file = "captures/" + file

            # load the capture
            lines = []
            prev_line = None
            f = pickle.load(open(file, "rb"))
            for line in f:
                if prev_line is None:
                    prev_line = line
                    continue

                now_time = line[1]
                prev_time = prev_line[1]

                dur = float(now_time - prev_time)

                out = parse_line(prev_line, dur)

                lines.append(out)

                prev_line = line

                if flag:
                    break

            # write the final line
            out = parse_line(prev_line, 0)
            lines.append(out)

            wait_play()
            print(f'Playing `{file.split(".")[0].replace("_", " ")}`')

            # play the capture
            for line in lines:
                if flag:
                    break

                if line[0]:
                    win32api.keybd_event(*line[1])
                else:
                    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, line[1][0], line[1][1], 0, 0)

                time.sleep(line[2])
    finally:
        # release all keys
        for k in [
            "w", "a", "s", "d",
            "space", "alt",
            "e", "q", "r", "f",
            "tab", "esc",
            "1", "2",
            "shift", "left_shift", "right_shift",
            "ctrl", "left_ctrl", "right_ctrl",
        ]:
            press_up(k)
        print("Released all keys")

        """
        """
