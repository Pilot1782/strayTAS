# Stray Tool Assisted Speedrun (TAS)

This is a tool assisted speedrun of Stray, a game by BlueTwelve Studio. The TAS was created using the included scripts.

## Running the TAS

1. Clone the repository
2. Install [Python 3](https://www.python.org/downloads/)
3. Install requirements: `pip install -r requirements.txt`
4. Run the TAS: `python main.py`

## Creating a TAS

1. Simply run `python capture.py` then press `ESC` to stop recording.
2. The result will be saved to `captures/out.txt`

## Playing back a TAS

1. Run `python main.py --play <path to TAS file>`

## Format of TAS file

The TAS file is a simple text file with the following format:

```
<key up/down> <key code> <timestamp starting from 0> <any additional notes>
# comments are also supported
```

For example:

```
\/ 65 0
# a is about to be released
/\ 65 0.1
```

Key codes can be found [here](https://docs.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes).

**NB: The key codes in the provided document are in hexadecimal, but the tool expects them in decimal, i.e. 0x41 = 65.**
