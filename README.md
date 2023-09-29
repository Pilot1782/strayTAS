# Stray Tool Assisted Speedrun (TAS)

This is a tool assisted speedrun of Stray, a game by BlueTwelve Studio. The TAS was created using the included scripts.

## Running the TAS

1. Clone the repository
2. Install [Python 3](https://www.python.org/downloads/)
3. Install requirements: `pip install -r requirements.txt`
4. Edit the following settings:

`Run` -> `Left Ctrl` (or any other key besides `shift`)
`Auto Camera` -> `O`

5. Run the TAS: `python main.py`

## Creating a TAS

1. Simply run `python capture.py` then press `ESC` to stop recording.
2. The result will be saved to `captures/out.txt`

## Playing back a TAS

1. Run `python main.py --play <path to TAS file>`
2. Note: there is about 0.0006s (+/-0.0001) of error per key action

## Editing a TAS

1. Open the TAS file with `tasEditor.py`
2. The format is described in the header of `capture.py` [here](capture.py#L13-L34)

Key codes can be found [here](https://docs.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes).

**NB: The key codes in the provided document are in hexadecimal, but the tool expects them in decimal, i.e. 0x41 = 65.**
