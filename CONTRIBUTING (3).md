# Contributing to PocketDeck

Thank you for your interest in improving PocketDeck.
This guide explains how to contribute in a way that keeps the project
accessible to beginners.

## Ground Rules

- All firmware code must stay in MicroPython. No C or C++ in the firmware folder.
  The whole point of this project is that beginners can read and edit it without
  a complex toolchain.

- Comments are mandatory. Every function and every non-obvious line should have
  a comment explaining what it does. Assume the reader has never written Python before.

- Do not introduce new dependencies unless they are absolutely necessary.
  The fewer libraries someone needs to install, the better.

## How to Contribute

1. Fork the repository on GitHub.
2. Create a branch with a short descriptive name, for example: `add-oled-support` or `fix-debounce`.
3. Make your changes.
4. Test on real hardware if possible. If you do not have the hardware, note that in your pull request.
5. Open a pull request with a description of what you changed and why.

## What Contributions Are Welcome

- Support for different displays (OLED SSD1306, larger TFT panels)
- Additional pre-built profiles for popular applications
- Improvements to the wiring diagram or documentation
- Case designs for different form factors
- Bug fixes for button debounce or display glitches
- A companion desktop app for profile editing (any language, any framework)

## What to Discuss Before Starting

If your change is large (new hardware support, major refactor, PCB design),
please open a GitHub Issue first to discuss the approach before writing code.
This avoids situations where you invest a lot of time in a direction
that does not fit the project.

## Code Style

- Use 4-space indentation.
- Keep lines under 100 characters.
- Use descriptive variable names. Avoid single-letter names except for loop counters.
- Write comments in plain English. No jargon.

## Reporting Bugs

Open a GitHub Issue and include:
- What hardware you are using (Pico version, display part number)
- What MicroPython version is installed
- The exact error message from Thonny's console
- What you expected to happen and what actually happened
