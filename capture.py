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


def process_key_press(key):
    t_press = time.time()
    if key == Key.esc:
        return False

    key_name = str(key).replace("'", "").replace("Key.", "").lower()

    if out and out[-1][0:4] == "\\/ " + key_name:
        return

    global start
    if start == -1:
        start = t_press

    out.append("\\/ " + key_name + " " + str(round(t_press - start, 3)))


def on_release(key):
    out.append(
        "/\\ "
        + str(key).replace("'", "").replace("Key.", "").lower()
        + " " + str(round(time.time() - start, 3))
    )


try:
    start = -1
    with Listener(
            on_press=process_key_press,
            on_release=on_release) as listener:
        listener.join()
finally:
    with open("captures/out.txt", "w") as f:
        f.write("\n".join(out))
