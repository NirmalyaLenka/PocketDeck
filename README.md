# PocketDeck

A DIY macro controller inspired by the Steam Deck, built around the Raspberry Pi Pico.
PocketDeck gives you 16 physical buttons, each mapped to a hotkey or application action,
plus a small color TFT display that shows which profile is active and what each button does.
The entire project is open source, beginner-friendly, and costs under $25 to build.

---

## What It Does

- 16 physical buttons arranged in a 4x4 grid
- Each button triggers a keyboard shortcut, media command, or application launch
- A 1.8-inch color TFT screen shows the active profile name and button labels
- Multiple profiles (Gaming, Coding, Media, Browser) switchable with a dedicated button
- The display updates instantly when you switch profiles
- Works on Windows, macOS, and Linux with no extra drivers
- Fully programmable in MicroPython, no C compiler needed

---

## Why This Project

Dedicated macro pads on the market cost $80 to $200. This project builds something comparable
for under $25 using a Raspberry Pi Pico, a cheap TFT display, and standard tactile switches.
The code is written in MicroPython so beginners can read and edit it without a complex toolchain.

---

## Hardware Required

| Part | Approximate Cost (USD) | Notes |
|---|---|---|
| Raspberry Pi Pico (not W) | $4 | The RP2040 chip handles everything |
| 1.8-inch ST7735 TFT Display | $3-5 | 128x160 pixels, SPI interface |
| 16x Tactile Push Buttons (6x6mm) | $2 | Standard breadboard buttons |
| 10x 10k Ohm Resistors | $1 | Pull-down resistors for buttons |
| Breadboard or Custom PCB | $2-5 | Breadboard works fine for prototyping |
| Micro USB Cable | $1 | For power and data |
| Jumper Wires | $1-2 | Standard male-to-male dupont wires |
| Optional: 3D Printed or Cardboard Case | $0-3 | STL files included in /hardware |

**Total: approximately $14 to $23**

---

## Wiring Overview

The display uses SPI. The buttons use direct GPIO pins with pull-down resistors.

### TFT Display Connections

```
TFT Pin    Pico Pin    GPIO
VCC        3V3 (36)    -
GND        GND (38)    -
SCL        Pin 6       GP4 (SPI0 SCK)
SDA        Pin 5       GP3 (SPI0 TX)
RES        Pin 7       GP5
DC         Pin 9       GP6
CS         Pin 10      GP7
BL         3V3 (36)    - (backlight always on)
```

### Button Matrix (16 buttons, each to its own GPIO)

```
Button 1   GP8     Button 2   GP9     Button 3   GP10    Button 4   GP11
Button 5   GP12    Button 6   GP13    Button 7   GP14    Button 8   GP15
Button 9   GP16    Button 10  GP17    Button 11  GP18    Button 12  GP19
Button 13  GP20    Button 14  GP21    Button 15  GP22    Button 16  GP26
```

Each button connects between its GPIO pin and GND.
A 10k pull-down resistor goes from each GPIO pin to GND.
The Pico's internal pull-up can be used instead if you want to skip external resistors
(in that case, wire buttons between GPIO and GND and change PULL_DOWN to PULL_UP in code).

A full wiring diagram image is in `/docs/images/wiring_diagram.png`.

---

## Software Setup

### Step 1: Install MicroPython on the Pico

1. Download the latest MicroPython UF2 file from https://micropython.org/download/rp2-pico/
2. Hold the BOOTSEL button on the Pico while plugging it into USB
3. A drive called RPI-RP2 will appear on your computer
4. Drag the downloaded .uf2 file onto that drive
5. The Pico will reboot automatically with MicroPython installed

### Step 2: Install Thonny (Beginner-Friendly IDE)

Thonny is the easiest way to write code and transfer files to the Pico.

1. Download Thonny from https://thonny.org
2. Open Thonny
3. In the bottom-right corner, click the interpreter selector and choose "MicroPython (Raspberry Pi Pico)"
4. Connect the Pico via USB

### Step 3: Copy the st7735.py Driver

The TFT display needs a driver library.

1. Open `firmware/st7735.py` from this repository in Thonny
2. Click File > Save As
3. Choose "Raspberry Pi Pico" as the destination
4. Save it as `st7735.py`

### Step 4: Copy the Main Firmware

1. Open `firmware/main.py` in Thonny
2. Save it to the Pico as `main.py`
3. Open `firmware/profiles.py` in Thonny
4. Save it to the Pico as `profiles.py`

### Step 5: Run It

Unplug and replug the Pico. It will start automatically because the file is named `main.py`.
You should see the display light up with the default profile name and button labels.

---

## How to Customize Button Actions

Open `firmware/profiles.py`. Each profile is a Python dictionary.
The keys are button numbers (1 through 16). The values are the actions to send.

```python
PROFILES = {
    "Gaming": {
        1: ("key", "F1"),         # Press F1
        2: ("key", "ctrl+c"),     # Copy
        3: ("key", "ctrl+v"),     # Paste
        4: ("media", "play"),     # Play/Pause media
        # ... and so on
    },
    "Coding": {
        1: ("key", "ctrl+shift+p"),   # Command palette (VS Code)
        2: ("key", "ctrl+/"),         # Toggle comment
        # ...
    }
}
```

To add a new profile, add a new dictionary entry with any name you like.
To change a button, replace the action tuple with your desired shortcut.
Supported action types are explained inside `profiles.py` with comments.

---

## Project File Structure

```
PocketDeck/
├── README.md                  This file
├── firmware/
│   ├── main.py                Entry point, main loop, button scanning
│   ├── profiles.py            All button mappings and profiles
│   ├── display_manager.py     Handles all TFT drawing and updates
│   └── st7735.py              Third-party TFT driver (MIT licensed)
├── hardware/
│   ├── pocketdeck_case.stl    3D printable enclosure
│   └── bom.csv                Full bill of materials with supplier links
├── host_software/
│   └── README.md              Optional PC-side companion app instructions
└── docs/
    └── images/
        └── wiring_diagram.png  Full wiring reference
```

---

## Troubleshooting

**Display shows nothing after power on**

Check that VCC is connected to 3V3 on the Pico, not 5V. The ST7735 is a 3.3V device.
Confirm SCL, SDA, RES, DC, and CS are connected to the correct GPIO pins.
Make sure `st7735.py` is saved on the Pico, not just on your computer.

**Buttons do not respond**

Check that pull-down resistors are in place (10k from GPIO pin to GND).
Open Thonny's REPL and run this to test a single button manually:

```python
from machine import Pin
btn = Pin(8, Pin.IN, Pin.PULL_DOWN)
print(btn.value())   # Should print 1 when button is held, 0 when released
```

**Pico not recognized by Thonny**

Try a different USB cable. Some cables are charge-only and have no data wires.
Make sure you selected "MicroPython (Raspberry Pi Pico)" in Thonny's interpreter settings.

**Profile switching button does nothing**

Button 16 (GP26) is reserved as the profile cycle button in the default firmware.
If you rewired it, update the `PROFILE_BUTTON` constant in `main.py`.

---

## Contributing

Pull requests are welcome. If you wire PocketDeck to a different display or add new features,
open an issue first to discuss the approach. Please keep all code in MicroPython so the project
stays accessible to beginners.

---

## License

MIT License. See LICENSE for full text.
You are free to use, modify, and distribute this project for personal or commercial purposes.

---

## Credits

- ST7735 MicroPython driver based on work by Boochow (MIT licensed)
- Inspired by the open macro pad community and the Steam Deck's approachable UI
