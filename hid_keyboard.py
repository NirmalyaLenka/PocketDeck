# hid_keyboard.py
# PocketDeck - USB HID keyboard and media key sender
#
# This file translates human-readable key names like "ctrl+c" or "F5"
# into the raw USB HID keycodes that the Raspberry Pi Pico sends over USB.
#
# The Pico appears to the computer as a USB keyboard, so no drivers are needed.
# This works on Windows, macOS, and Linux out of the box.
#
# You should not need to edit this file unless you want to add support for
# keys that are not listed in KEYCODE_MAP below.

import usb_hid
from adafruit_hid.keyboard import Keyboard as HIDKeyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

# ─── Key name to HID keycode mapping ─────────────────────────────────────────
#
# Add entries here if you need a key that is not listed.
# All keys from Keycode are valid. See:
# https://docs.circuitpython.org/projects/hid/en/latest/api.html#adafruit_hid.keycode.Keycode

KEYCODE_MAP = {
    # Letters
    "a": Keycode.A, "b": Keycode.B, "c": Keycode.C, "d": Keycode.D,
    "e": Keycode.E, "f": Keycode.F, "g": Keycode.G, "h": Keycode.H,
    "i": Keycode.I, "j": Keycode.J, "k": Keycode.K, "l": Keycode.L,
    "m": Keycode.M, "n": Keycode.N, "o": Keycode.O, "p": Keycode.P,
    "q": Keycode.Q, "r": Keycode.R, "s": Keycode.S, "t": Keycode.T,
    "u": Keycode.U, "v": Keycode.V, "w": Keycode.W, "x": Keycode.X,
    "y": Keycode.Y, "z": Keycode.Z,

    # Numbers (top row)
    "0": Keycode.ZERO,  "1": Keycode.ONE,   "2": Keycode.TWO,
    "3": Keycode.THREE, "4": Keycode.FOUR,  "5": Keycode.FIVE,
    "6": Keycode.SIX,   "7": Keycode.SEVEN, "8": Keycode.EIGHT,
    "9": Keycode.NINE,

    # Function keys
    "f1":  Keycode.F1,  "f2":  Keycode.F2,  "f3":  Keycode.F3,
    "f4":  Keycode.F4,  "f5":  Keycode.F5,  "f6":  Keycode.F6,
    "f7":  Keycode.F7,  "f8":  Keycode.F8,  "f9":  Keycode.F9,
    "f10": Keycode.F10, "f11": Keycode.F11, "f12": Keycode.F12,

    # Navigation and editing
    "escape":      Keycode.ESCAPE,
    "space":       Keycode.SPACE,
    "enter":       Keycode.ENTER,
    "return":      Keycode.ENTER,
    "backspace":   Keycode.BACKSPACE,
    "delete":      Keycode.DELETE,
    "tab":         Keycode.TAB,
    "up":          Keycode.UP_ARROW,
    "down":        Keycode.DOWN_ARROW,
    "left":        Keycode.LEFT_ARROW,
    "right":       Keycode.RIGHT_ARROW,
    "home":        Keycode.HOME,
    "end":         Keycode.END,
    "pageup":      Keycode.PAGE_UP,
    "pagedown":    Keycode.PAGE_DOWN,
    "insert":      Keycode.INSERT,
    "printscreen": Keycode.PRINT_SCREEN,
    "scrolllock":  Keycode.SCROLL_LOCK,
    "pause":       Keycode.PAUSE,

    # Symbols (US layout)
    "grave":      Keycode.GRAVE_ACCENT,   # ` key (also used for VS Code terminal)
    "minus":      Keycode.MINUS,
    "plus":       Keycode.EQUALS,         # The = key, Shift makes +
    "equals":     Keycode.EQUALS,
    "leftbracket": Keycode.LEFT_BRACKET,
    "rightbracket": Keycode.RIGHT_BRACKET,
    "backslash":  Keycode.BACKSLASH,
    "semicolon":  Keycode.SEMICOLON,
    "quote":      Keycode.QUOTE,
    "comma":      Keycode.COMMA,
    "period":     Keycode.PERIOD,
    "slash":      Keycode.FORWARD_SLASH,
}

# Modifier key names to HID keycodes.
MODIFIER_MAP = {
    "ctrl":   Keycode.LEFT_CONTROL,
    "control": Keycode.LEFT_CONTROL,
    "shift":  Keycode.LEFT_SHIFT,
    "alt":    Keycode.LEFT_ALT,
    "option": Keycode.LEFT_ALT,    # macOS alt key alias
    "cmd":    Keycode.LEFT_GUI,    # macOS command key
    "gui":    Keycode.LEFT_GUI,    # Windows key on Windows
    "win":    Keycode.LEFT_GUI,
    "meta":   Keycode.LEFT_GUI,
}

# Media control codes.
MEDIA_MAP = {
    "play":        ConsumerControlCode.PLAY_PAUSE,
    "next":        ConsumerControlCode.SCAN_NEXT_TRACK,
    "prev":        ConsumerControlCode.SCAN_PREVIOUS_TRACK,
    "stop":        ConsumerControlCode.STOP,
    "mute":        ConsumerControlCode.MUTE,
    "volume_up":   ConsumerControlCode.VOLUME_INCREMENT,
    "volume_down": ConsumerControlCode.VOLUME_DECREMENT,
    "brightness_up":   ConsumerControlCode.BRIGHTNESS_INCREMENT,
    "brightness_down": ConsumerControlCode.BRIGHTNESS_DECREMENT,
}


# ─── Keyboard class ──────────────────────────────────────────────────────────

class Keyboard:
    """
    Provides send_key, send_media_key, and type_string methods.
    This wraps the Adafruit HID library so the rest of PocketDeck does not
    need to think about raw keycodes.
    """

    def __init__(self, hid_devices):
        self.kbd    = HIDKeyboard(hid_devices)
        self.layout = KeyboardLayoutUS(self.kbd)
        self.cc     = ConsumerControl(hid_devices)

    def send_key(self, key_name, modifiers=None):
        """
        Sends a key press with optional modifier keys, then releases all keys.

        key_name:  string from KEYCODE_MAP (e.g. "c", "f5", "space")
        modifiers: list of strings from MODIFIER_MAP (e.g. ["ctrl", "shift"])
        """
        if modifiers is None:
            modifiers = []

        keys_to_press = []

        # Resolve modifier keys.
        for mod in modifiers:
            code = MODIFIER_MAP.get(mod.lower())
            if code is not None:
                keys_to_press.append(code)
            else:
                print("Warning: unknown modifier:", mod)

        # Resolve main key.
        main_code = KEYCODE_MAP.get(key_name.lower())
        if main_code is not None:
            keys_to_press.append(main_code)
        else:
            print("Warning: unknown key name:", key_name)
            return

        # Press and release.
        self.kbd.send(*keys_to_press)

    def send_media_key(self, media_key_name):
        """
        Sends a consumer control (media) key.
        media_key_name: string from MEDIA_MAP (e.g. "play", "volume_up")
        """
        code = MEDIA_MAP.get(media_key_name.lower())
        if code is not None:
            self.cc.send(code)
        else:
            print("Warning: unknown media key:", media_key_name)

    def type_string(self, text):
        """
        Types a string of text as if it were typed on the keyboard.
        Supports printable ASCII characters.
        """
        self.layout.write(text)
