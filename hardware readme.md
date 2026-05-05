# Hardware

This folder contains the physical build files for PocketDeck.

## Files

### bom.csv

The complete bill of materials with part descriptions, quantities, approximate costs,
and example suppliers. Open this in any spreadsheet app or text editor.

### pocketdeck_case.stl

A 3D-printable enclosure designed to hold:
- One Raspberry Pi Pico (micro USB facing right side)
- One 1.8-inch TFT display (cutout in the top-left corner)
- A 4x4 grid of 6x6mm tactile buttons (16 button holes)

Print settings that work well:
- Material: PLA
- Layer height: 0.2mm
- Infill: 20%
- Supports: Not required
- Estimated print time: 2 to 3 hours

If you do not have a 3D printer, a cardboard or wooden box works fine for prototyping.
Cut button holes with a craft knife and use hot glue to hold parts in place.

## Wiring Notes

The full wiring diagram is in `/docs/images/wiring_diagram.png`.

Key points to remember during assembly:

1. The TFT display runs on 3.3V. Connecting it to the 5V VBUS pin will damage it.
   Use the 3V3 output pin (pin 36) on the Pico.

2. Pull-down resistors are required for each button GPIO.
   Without them the pin floats and will randomly trigger.
   A 10k resistor from GPIO to GND on each button is the standard solution.

3. The Pico does not need any additional power circuitry.
   USB power from your computer is enough for all 16 buttons and the display.

4. If you plan to use a custom PCB, the Gerber files are not yet included
   in this release. They are planned for a future version.
   For now, a breadboard or perfboard build is the recommended approach.
