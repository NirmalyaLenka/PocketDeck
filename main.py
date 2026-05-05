# main.py
# PocketDeck - Main entry point and button scanning loop
#
# This file runs automatically when the Pico powers on because it is named main.py.
# It sets up the buttons, initializes the display, loads profiles, and
# enters a loop that checks for button presses and sends HID commands.
#
# If you want to change the pin assignments, edit the GPIO numbers in this file.
# If you want to change what buttons do, edit profiles.py instead.

import time
import usb_hid
from machine import Pin, SPI
from hid_keyboard import Keyboard
from display_manager import DisplayManager
from profiles import PROFILES, PROFILE_ORDER

# ─── Configuration ─────────────────────────────────────────────────────────────

# GPIO pins for each of the 16 buttons, in order from button 1 to button 16.
# Button 16 is reserved as the profile cycle button (see PROFILE_BUTTON below).
BUTTON_PINS = [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 26]

# This button cycles through profiles instead of sending a keyboard shortcut.
PROFILE_BUTTON = 16   # button number (1-indexed), not GPIO number

# How long to wait after a button is pressed before accepting another press.
# This prevents accidental double-presses. Value is in milliseconds.
DEBOUNCE_MS = 150

# SPI display pins (must match your wiring).
SPI_SCK  = 4
SPI_MOSI = 3
SPI_CS   = 7
TFT_RST  = 5
TFT_DC   = 6

# ─── Setup ─────────────────────────────────────────────────────────────────────

def setup_buttons(pin_list):
    """
    Create Pin objects for all buttons with internal pull-down resistors.
    If you wired buttons between GPIO and VCC instead of GND, change
    Pin.PULL_DOWN to Pin.PULL_UP and invert the check in the main loop.
    """
    buttons = []
    for gpio_num in pin_list:
        pin = Pin(gpio_num, Pin.IN, Pin.PULL_DOWN)
        buttons.append(pin)
    return buttons


def setup_display():
    """
    Initialize the SPI bus and return a DisplayManager instance.
    The DisplayManager handles all drawing so this file stays clean.
    """
    spi = SPI(0,
              baudrate=20_000_000,
              polarity=0,
              phase=0,
              sck=Pin(SPI_SCK),
              mosi=Pin(SPI_MOSI))
    dm = DisplayManager(spi,
                        cs_pin=SPI_CS,
                        rst_pin=TFT_RST,
                        dc_pin=TFT_DC)
    return dm


# ─── Main loop ─────────────────────────────────────────────────────────────────

def main():
    buttons   = setup_buttons(BUTTON_PINS)
    display   = setup_display()
    keyboard  = Keyboard(usb_hid.devices)

    current_profile_index = 0
    last_press_time       = 0

    # Show the first profile on the display when the device boots.
    profile_name = PROFILE_ORDER[current_profile_index]
    display.draw_profile(profile_name, PROFILES[profile_name])

    print("PocketDeck ready. Active profile:", profile_name)

    while True:
        now = time.ticks_ms()

        for index, btn in enumerate(buttons):
            button_number = index + 1   # convert 0-indexed list to 1-indexed

            if btn.value() == 1:        # button is pressed (PULL_DOWN: 1 = pressed)

                # Debounce: ignore if a button was already pressed very recently.
                if time.ticks_diff(now, last_press_time) < DEBOUNCE_MS:
                    continue

                last_press_time = now

                # Profile cycle button: rotate through profiles.
                if button_number == PROFILE_BUTTON:
                    current_profile_index = (current_profile_index + 1) % len(PROFILE_ORDER)
                    profile_name = PROFILE_ORDER[current_profile_index]
                    display.draw_profile(profile_name, PROFILES[profile_name])
                    print("Switched to profile:", profile_name)

                else:
                    # Regular button: look up the action in the current profile.
                    profile_name = PROFILE_ORDER[current_profile_index]
                    action = PROFILES[profile_name].get(button_number)

                    if action is not None:
                        action_type, action_value = action
                        execute_action(keyboard, action_type, action_value)
                        print("Button", button_number, "->", action_type, action_value)
                    else:
                        print("Button", button_number, "has no action in profile", profile_name)

        # Short sleep keeps the loop from hammering the CPU at 100%.
        time.sleep_ms(10)


def execute_action(keyboard, action_type, action_value):
    """
    Sends the appropriate HID event based on the action type.

    action_type can be:
      "key"    - sends a keyboard shortcut (e.g. "ctrl+c", "F5", "a")
      "media"  - sends a media key (e.g. "play", "next", "volume_up")
      "text"   - types a string of text character by character

    action_value is a string describing the key or text to send.
    """
    if action_type == "key":
        # Parse modifier keys out of strings like "ctrl+shift+p"
        parts     = action_value.lower().split("+")
        main_key  = parts[-1]
        modifiers = parts[:-1]
        keyboard.send_key(main_key, modifiers)

    elif action_type == "media":
        keyboard.send_media_key(action_value)

    elif action_type == "text":
        keyboard.type_string(action_value)

    else:
        print("Unknown action type:", action_type)


# ─── Entry ─────────────────────────────────────────────────────────────────────

main()
