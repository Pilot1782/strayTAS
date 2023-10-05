import argparse
import pickle
import queue
import subprocess
import sys
import threading
import time

import keyboard
import win32gui
from pynput.keyboard import Listener, Key, KeyCode

from keys import VK_CODE

KV_CODE = {v: k for k, v in VK_CODE.items()}

out = queue.Queue()
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

record = False
_exit = False
start = -1
last_mouse = None
last_key = None
ignore = [
    Key.f1, Key.f2,
    Key.esc
]


def add_mouse(t: float, dx: int, dy: int):
    out.put((
        0x02,
        t - start,
        dx,
        dy,
    ))


def check_press(key):
    t = time.time()
    global record
    global start
    global last_key

    if record:
        if key == Key.esc:
            out.put((
                0x00,
                t - start,
                0x1B,
                0,
                "esc"
            ))
        else:
            code = key.vk if hasattr(key, "vk") else key.value.vk
            name = KV_CODE[code]

            if last_key is None:
                last_key = (code, name)
            elif last_key == (code, name):
                return
            else:
                last_key = (code, name)

            out.put((
                0x00,
                t - start,
                int(code),
                0,
                name
            ))


def check_release(key: Key | KeyCode):
    global last_key

    if record is False:
        return

    code = key.vk if hasattr(key, "vk") else key.value.vk
    name = KV_CODE[code]

    if last_key == (code, name):
        last_key = None

    out.put((
        0x01,
        time.time() - start,
        int(code),
        0,
        name
    ))


def handle_keys():
    """
    Handle key presses as a thread
    :return:
    """

    with Listener(on_press=check_press, on_release=check_release) as listener:
        listener.join()


def handle_mouse():
    """
    Handle mouse movement as a thread
    :return:
    """
    global last_mouse

    while _exit is False:
        time.sleep(0.1)

        if record:
            x, y = win32gui.GetCursorPos()
            t = time.time()
            if last_mouse is None:
                last_mouse = (x, y)
            elif (x, y) != last_mouse:
                dx = x - last_mouse[0]
                dy = y - last_mouse[1]

                last_mouse = (x, y)
                add_mouse(t, dx, dy)
        else:
            time.sleep(0.1)


def main():
    print("Press F1 to start recording, F2 to exit")

    key_thread = threading.Thread(target=handle_keys)
    mouse_thread = threading.Thread(target=handle_mouse)

    key_thread.start()
    mouse_thread.start()


def save(path: str = None):
    global record, _exit
    print("Saving...")
    record = False
    _exit = True
    if path is None:
        path = "captures/out.pkl"

    pickle.dump(list(out.queue), open(path, "wb"))
    print("Saved!")
    sys.exit(0)


if __name__ == "__main__":
    argparse.ArgumentParser()
    parser = argparse.ArgumentParser(description="Record key presses and mouse movements")
    parser.add_argument("--cap", type=str, help="Run a file and save the resutl to a file")

    args = parser.parse_args()


    def toggle_record():
        global record
        record = not record
        print(f"Recording: {record}")


    # register key binds
    keyboard.add_hotkey(hotkey="f1", callback=toggle_record)
    keyboard.add_hotkey(hotkey="f2", callback=save)
    keyboard.add_hotkey(hotkey="esc", callback=save)

    main()
    proc = None

    if args.cap is not None:
        proc = subprocess.Popen([args.cap, "--sub"])

    while not _exit:
        time.sleep(0.1)

    if args.cap is not None:
        proc.kill()

    save(None if args.cap is None else "out.pkl")
