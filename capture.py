import subprocess
import sys
import time

from pynput.keyboard import Listener, Key

out = []

"""
Format of output:
```
\/ <key> <time>
/\ <key> <time>
```

<time> will always start at 0
    units are seconds
    
`/\` indicated that <key> was released
`\/` indicated that <key> was pressed down

EX:
```
\/ a 0.0
/\ a 0.1
```

ie: `a` was held for 0.1 seconds
"""

flag = False


def key_to_code(key):
    tp = str(type(key))
    key_code = key.value if tp == "<enum 'Key'>" else key
    return str(key_code.vk)


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

    if out and out[-1][0:4] == "\\/ " + key_value:
        return

    global start
    if start == -1:
        start = t_press

    out.append(
        "\\/ "
        + key_value
        + " " + str(round(t_press - start, 3))
        + " " + key_to_name(key)
    )


def on_release(key):
    key_value = key_to_code(key)

    out.append(
        "/\\ "
        + key_value
        + " " + str(round(time.time() - start, 3))
        + " " + key_to_name(key)
    )


def main_greedy():
    try:
        global start
        start = -1
        with Listener(
                on_press=process_key_press,
                on_release=on_release) as listener:
            listener.join()
    finally:
        with open("captures/out.txt", "w") as f:
            f.write("\n".join(out))


def main():
    try:
        global start
        start = -1
        listener = Listener(
            on_press=process_key_press,
            on_release=on_release)
        listener.start()
    finally:
        ...


if __name__ == "__main__":
    args = sys.argv[1:]

    if args and args[0] == "--cap":
        print("Capturing...")

        main()

        pip = subprocess.Popen(["python", *args[1:], "--sub"])

        while pip.poll() is None and not flag:
            time.sleep(0.1)

        pip.kill()

        with open("captures/out.txt", "w") as f:
            f.write("\n".join(out))
    else:
        main_greedy()
