# display_manager.py
# PocketDeck - TFT display drawing and layout
#
# This file handles everything visual on the ST7735 1.8-inch TFT display.
# The display is 128 pixels wide and 160 pixels tall.
#
# The screen layout is:
#   Line 1 (top):        Profile name in large text, white on colored background
#   Lines 2-5 (middle):  4x4 grid of button labels, one per button slot
#   Line 6 (bottom):     "BTN 16: Switch Profile" reminder
#
# You do not need to edit this file unless you want to change colors or layout.
# Button labels shown on screen come from the profile name + button number.

from machine import Pin
import st7735

# ─── Color constants (RGB565 format used by ST7735) ───────────────────────────

BLACK   = 0x0000
WHITE   = 0xFFFF
RED     = 0xF800
GREEN   = 0x07E0
BLUE    = 0x001F
CYAN    = 0x07FF
MAGENTA = 0xF81F
YELLOW  = 0xFFE0
ORANGE  = 0xFC00
GRAY    = 0x8410
DARK    = 0x18E3

# Profile name banner colors (background, text).
# You can change these to any RGB565 color pairs you like.
PROFILE_COLORS = {
    "Gaming":  (RED,    WHITE),
    "Coding":  (BLUE,   WHITE),
    "Media":   (MAGENTA, WHITE),
    "Browser": (GREEN,  BLACK),
}
DEFAULT_BANNER_COLOR = (DARK, WHITE)

# ─── DisplayManager ───────────────────────────────────────────────────────────

class DisplayManager:
    """
    Wraps the ST7735 driver and provides high-level drawing methods for PocketDeck.

    Usage:
        dm = DisplayManager(spi, cs_pin=7, rst_pin=5, dc_pin=6)
        dm.draw_profile("Gaming", PROFILES["Gaming"])
    """

    # Display dimensions for the 1.8-inch ST7735.
    WIDTH  = 128
    HEIGHT = 160

    def __init__(self, spi, cs_pin, rst_pin, dc_pin):
        self.tft = st7735.ST7735(
            spi,
            cs   = Pin(cs_pin,  Pin.OUT),
            rst  = Pin(rst_pin, Pin.OUT),
            dc   = Pin(dc_pin,  Pin.OUT),
            width  = self.WIDTH,
            height = self.HEIGHT,
        )
        self.tft.init()
        self.tft.fill(BLACK)

    # ─── Public methods ────────────────────────────────────────────────────────

    def draw_profile(self, profile_name, profile_dict):
        """
        Redraws the entire screen for a given profile.

        profile_name:  string, e.g. "Gaming"
        profile_dict:  the dictionary from profiles.py for this profile
        """
        self.tft.fill(BLACK)
        self._draw_banner(profile_name)
        self._draw_button_grid(profile_dict)
        self._draw_footer()

    def draw_message(self, line1, line2=""):
        """
        Draws a simple two-line centered message. Used for boot screen or errors.
        """
        self.tft.fill(BLACK)
        self._draw_text_centered(line1, y=60, color=WHITE, scale=2)
        if line2:
            self._draw_text_centered(line2, y=84, color=GRAY, scale=1)

    # ─── Private drawing helpers ───────────────────────────────────────────────

    def _draw_banner(self, profile_name):
        """
        Draws the colored banner at the top with the profile name.
        """
        bg, fg = PROFILE_COLORS.get(profile_name, DEFAULT_BANNER_COLOR)

        # Fill banner rectangle: full width, 24 pixels tall.
        self.tft.fill_rect(0, 0, self.WIDTH, 24, bg)

        # Center the text inside the banner.
        text = profile_name.upper()
        # Each character in scale=2 is approximately 12 pixels wide, 16 tall.
        text_width = len(text) * 12
        x = max(0, (self.WIDTH - text_width) // 2)
        self.tft.text(text, x, 4, fg, size=2)

    def _draw_button_grid(self, profile_dict):
        """
        Draws button labels in a 4x4 grid below the banner.

        The grid starts at y=28 and each cell is 32x32 pixels.
        Button numbers go left-to-right, top-to-bottom:
          1  2  3  4
          5  6  7  8
          9 10 11 12
         13 14 15 16
        """
        CELL_W = 32
        CELL_H = 32
        GRID_X = 0
        GRID_Y = 28

        for row in range(4):
            for col in range(4):
                button_num = row * 4 + col + 1
                cell_x = GRID_X + col * CELL_W
                cell_y = GRID_Y + row * CELL_H

                # Draw cell border.
                self.tft.rect(cell_x, cell_y, CELL_W, CELL_H, GRAY)

                # Draw button number in top-left of cell.
                num_label = str(button_num)
                self.tft.text(num_label, cell_x + 2, cell_y + 2, GRAY, size=1)

                # Draw action label in center of cell.
                action = profile_dict.get(button_num)
                if action is not None:
                    label = self._short_label(action)
                    lbl_x = cell_x + 2
                    lbl_y = cell_y + 14
                    self.tft.text(label, lbl_x, lbl_y, WHITE, size=1)
                else:
                    # Profile switch button or unassigned.
                    if button_num == 16:
                        self.tft.text(">>", cell_x + 8, cell_y + 14, YELLOW, size=1)
                    else:
                        self.tft.text("--", cell_x + 8, cell_y + 14, GRAY, size=1)

    def _draw_footer(self):
        """
        Draws a small reminder at the bottom that button 16 switches profiles.
        """
        y = self.HEIGHT - 10
        self.tft.fill_rect(0, y - 2, self.WIDTH, 12, DARK)
        self.tft.text("B16: Next Profile", 4, y, GRAY, size=1)

    def _draw_text_centered(self, text, y, color, scale=1):
        char_w = 8 * scale
        text_w = len(text) * char_w
        x = max(0, (self.WIDTH - text_w) // 2)
        self.tft.text(text, x, y, color, size=scale)

    # ─── Label formatting ──────────────────────────────────────────────────────

    def _short_label(self, action):
        """
        Converts an action tuple to a short display label that fits in a 30px cell.
        Labels are truncated or abbreviated so they fit on screen.
        """
        action_type, action_value = action

        if action_type == "media":
            # Map media keys to short symbols or abbreviations.
            MEDIA_LABELS = {
                "play":        "PLAY",
                "next":        "NEXT",
                "prev":        "PREV",
                "mute":        "MUTE",
                "volume_up":   "VOL+",
                "volume_down": "VOL-",
            }
            return MEDIA_LABELS.get(action_value, action_value[:4].upper())

        elif action_type == "key":
            # Shorten common modifier combos.
            label = action_value.upper()
            label = label.replace("CTRL+SHIFT+", "C+S+")
            label = label.replace("CTRL+", "C+")
            label = label.replace("ALT+", "A+")
            label = label.replace("SHIFT+", "S+")
            # Truncate to 4 characters so it fits in the cell.
            return label[:4]

        elif action_type == "text":
            return "TXT"

        else:
            return "???"
