# E-Ink Emulator

## How to run it
Clone the repo

`https://github.com/eric-hamilton/e-ink_emulator.git`

Enter the repo

`cd e-ink_emulator`

Create a virtual environment

`python -m venv venv`

Activate the virtual environment

`venv/Scripts/activate`

Install dependencies

`pip install -r requirements.txt`

Run the Program

`python run.py`


## Considerations
- The hardware code is pulled directly from some Waveshare E-paper library.
I use a hardcoded library for a 2.9 inch Waveshare epaper module. It won't work on most hardware out of the box.

- This uses a hella deprecated PIL module so the text sizing logic is kind of worthless

## How it works
- If you're not running the program on hardware, it will launch the emulator.

The `run.py` and `emulator/__init__.py` check if the logic is available for use on the Pi. If not, it runs the emulator.

### Screens
Screens are defined in `emulator/screens.py`. Each screen has an `update` function and an `update_interval` attribute. Once an update interval has elapsed, the main loop will call the `update` function on the current screen. That `update` function is where you'll build the display.

### The emulator
The emulator uses a tkinter window to mimic the resolution of the e-ink display. It takes the same arguments that the hardware panel does, which involves flashing a PIL image to the image buffer. There are also 3 buttons to emulate the 3 hardware GPIO buttons I have on the weatherstation

### Fonts
Add `.ttf` fonts to the `emulator/fonts` folder. To use them:

```
from emulator.fonts import create_font
create_font('some_font.ttf', 32)
```
`create_font` will handle the formatting for the canvas