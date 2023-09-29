import pickle
import subprocess
import sys
import threading
import time

import win32gui
from pynput.keyboard import Listener, Key

out = []
mouse = []

"""
Format of output:
```
[
    (0x00, <time>, <key code>, 0  , ...),
    (0x01, <time>, <key code>, 0  , ...),
    (0x02, <time>, <x>,        <y>, ...),
    ...
]
```

0x00 indicates a key press
0x01 indicates a key release
0x02 indicates a mouse movement (relative)

<time> will always start at 0
    units are seconds
<key code> is the key code of the key pressed (only used with 0x00|0x01)
<x> and <y> are the relative mouse movement (only used with 0x02)

anything after the first 4 elements is ignored
"""

flag = False


def key_to_code(key):
    tp = str(type(key))
    key_code = key.value if tp == "<enum 'Key'>" else key

    return key_code.vk


def key_to_name(key):
    tp = str(type(key))
    key_name = key.name if tp == "<enum 'Key'>" else key.char
    return key_name


def process_key_press(key):
    t_press = time.time()

    if key == Key.esc:
        global flag
        flag = True
        return False

    key_value = key_to_code(key)

    if out and [out[-1][0], out[-1][2]] == [0x00, key_value]:
        return

    global start
    if start == -1:
        start = t_press

    out.append((
        0x00,
        round(t_press - start, 4),
        key_value,
        0
    ))


def on_release(key):
    t = time.time()

    key_value = key_to_code(key)

    out.append((
        0x01,
        round(t - start, 4),
        key_value,
        0
    ))


def moved(x, y, t):
    global prev_pos
    dx = x - prev_pos[0]
    dy = y - prev_pos[1]
    print(f"Recorded mouse position: ({x}, {y}) ({dx}, {dy})")
    mouse.append((
        0x02,
        round(t - start, 3),
        dx,
        dy
    ))
    prev_pos = (x, y)


def check_mouse():
    global prev_pos
    while start == -1:
        time.sleep(0.1)

    while not flag:
        x, y = win32gui.GetCursorPos()
        t = time.time()
        if x != prev_pos[0] or y != prev_pos[1]:
            moved(x, y, t)
            prev_pos = (x, y)


def main():
    global start
    start = -1
    listener = Listener(
        on_press=process_key_press,
        on_release=on_release)
    listener.start()

    global prev_pos
    prev_pos = win32gui.GetCursorPos()
    threading.Thread(target=check_mouse).start()


if __name__ == "__main__":
    args = sys.argv[1:]
    print("Capturing...")
    main()

    if args and args[0] == "--cap":
        print(f"Running {' '.join(args[1:])}...")

        pip = subprocess.Popen(["python", *args[1:], "--sub"])

        while pip.poll() is None and not flag:
            time.sleep(0.1)

        pip.kill()

    while not flag:
        time.sleep(0.1)

    out.extend(mouse)
    out.sort(key=lambda _: _[1])

    pickle.dump(out, open("captures/out.pkl", "wb"))

"""
This is text that should be copied
"""
