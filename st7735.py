# st7735.py
# ST7735 TFT Display Driver for MicroPython
#
# This is a minimal driver for the ST7735 1.8-inch TFT display.
# Based on the work of Boochow (MIT License).
# Source: https://github.com/boochow/MicroPython-ST7735
#
# You do not need to read or modify this file.
# It is a hardware driver that translates drawing commands into
# the SPI byte sequences the ST7735 chip understands.
#
# Methods you can use from display_manager.py:
#   tft.fill(color)                     Fill entire screen with a color
#   tft.fill_rect(x, y, w, h, color)    Fill a rectangle
#   tft.rect(x, y, w, h, color)         Draw rectangle border only
#   tft.pixel(x, y, color)              Draw a single pixel
#   tft.text(string, x, y, color)       Draw text (scale defaults to 1)
#   tft.hline(x, y, w, color)           Horizontal line
#   tft.vline(x, y, h, color)           Vertical line

import time
from machine import Pin
import ustruct

# ST7735 command constants
_NOP       = 0x00
_SWRESET   = 0x01
_SLPOUT    = 0x11
_DISPOFF   = 0x28
_DISPON    = 0x29
_CASET     = 0x2A
_RASET     = 0x2B
_RAMWR     = 0x2C
_MADCTL    = 0x36
_COLMOD    = 0x3A
_FRMCTR1   = 0xB1
_FRMCTR2   = 0xB2
_FRMCTR3   = 0xB3
_INVCTR    = 0xB4
_PWCTR1    = 0xC0
_PWCTR2    = 0xC1
_PWCTR3    = 0xC2
_PWCTR4    = 0xC3
_PWCTR5    = 0xC4
_VMCTR1    = 0xC5
_GMCTRP1   = 0xE0
_GMCTRN1   = 0xE1

# Built-in 5x8 font (ASCII 32-127)
_FONT = (
    b'\x00\x00\x00\x00\x00', b'\x00\x00\x5f\x00\x00', b'\x00\x07\x00\x07\x00',
    b'\x14\x7f\x14\x7f\x14', b'\x24\x2a\x7f\x2a\x12', b'\x23\x13\x08\x64\x62',
    b'\x36\x49\x55\x22\x50', b'\x00\x05\x03\x00\x00', b'\x00\x1c\x22\x41\x00',
    b'\x00\x41\x22\x1c\x00', b'\x14\x08\x3e\x08\x14', b'\x08\x08\x3e\x08\x08',
    b'\x00\x50\x30\x00\x00', b'\x08\x08\x08\x08\x08', b'\x00\x60\x60\x00\x00',
    b'\x20\x10\x08\x04\x02', b'\x3e\x51\x49\x45\x3e', b'\x00\x42\x7f\x40\x00',
    b'\x42\x61\x51\x49\x46', b'\x21\x41\x45\x4b\x31', b'\x18\x14\x12\x7f\x10',
    b'\x27\x45\x45\x45\x39', b'\x3c\x4a\x49\x49\x30', b'\x01\x71\x09\x05\x03',
    b'\x36\x49\x49\x49\x36', b'\x06\x49\x49\x29\x1e', b'\x00\x36\x36\x00\x00',
    b'\x00\x56\x36\x00\x00', b'\x08\x14\x22\x41\x00', b'\x14\x14\x14\x14\x14',
    b'\x00\x41\x22\x14\x08', b'\x02\x01\x51\x09\x06', b'\x3e\x41\x5d\x55\x1e',
    b'\x7e\x09\x09\x09\x7e', b'\x7f\x49\x49\x49\x36', b'\x3e\x41\x41\x41\x22',
    b'\x7f\x41\x41\x22\x1c', b'\x7f\x49\x49\x49\x41', b'\x7f\x09\x09\x09\x01',
    b'\x3e\x41\x49\x49\x7a', b'\x7f\x08\x08\x08\x7f', b'\x00\x41\x7f\x41\x00',
    b'\x20\x40\x41\x3f\x01', b'\x7f\x08\x14\x22\x41', b'\x7f\x40\x40\x40\x40',
    b'\x7f\x02\x0c\x02\x7f', b'\x7f\x04\x08\x10\x7f', b'\x3e\x41\x41\x41\x3e',
    b'\x7f\x09\x09\x09\x06', b'\x3e\x41\x51\x21\x5e', b'\x7f\x09\x19\x29\x46',
    b'\x46\x49\x49\x49\x31', b'\x01\x01\x7f\x01\x01', b'\x3f\x40\x40\x40\x3f',
    b'\x1f\x20\x40\x20\x1f', b'\x3f\x40\x38\x40\x3f', b'\x63\x14\x08\x14\x63',
    b'\x07\x08\x70\x08\x07', b'\x61\x51\x49\x45\x43', b'\x00\x7f\x41\x41\x00',
    b'\x02\x04\x08\x10\x20', b'\x00\x41\x41\x7f\x00', b'\x04\x02\x01\x02\x04',
    b'\x40\x40\x40\x40\x40', b'\x00\x01\x02\x04\x00', b'\x20\x54\x54\x54\x78',
    b'\x7f\x48\x44\x44\x38', b'\x38\x44\x44\x44\x20', b'\x38\x44\x44\x48\x7f',
    b'\x38\x54\x54\x54\x18', b'\x08\x7e\x09\x01\x02', b'\x0c\x52\x52\x52\x3e',
    b'\x7f\x08\x04\x04\x78', b'\x00\x44\x7d\x40\x00', b'\x20\x40\x44\x3d\x00',
    b'\x7f\x10\x28\x44\x00', b'\x00\x41\x7f\x40\x00', b'\x7c\x04\x18\x04\x78',
    b'\x7c\x08\x04\x04\x78', b'\x38\x44\x44\x44\x38', b'\x7c\x14\x14\x14\x08',
    b'\x08\x14\x14\x18\x7c', b'\x7c\x08\x04\x04\x08', b'\x48\x54\x54\x54\x20',
    b'\x04\x3f\x44\x40\x20', b'\x3c\x40\x40\x20\x7c', b'\x1c\x20\x40\x20\x1c',
    b'\x3c\x40\x30\x40\x3c', b'\x44\x28\x10\x28\x44', b'\x0c\x50\x50\x50\x3c',
    b'\x44\x64\x54\x4c\x44', b'\x00\x08\x36\x41\x00', b'\x00\x00\x7f\x00\x00',
    b'\x00\x41\x36\x08\x00', b'\x10\x08\x08\x10\x08', b'\x00\x00\x00\x00\x00',
)


class ST7735:
    def __init__(self, spi, cs, rst, dc, width=128, height=160):
        self.spi    = spi
        self.cs     = cs
        self.rst    = rst
        self.dc     = dc
        self.width  = width
        self.height = height
        self.cs.init(self.cs.OUT, value=1)
        self.dc.init(self.dc.OUT, value=0)
        self.rst.init(self.rst.OUT, value=1)

    def _write_cmd(self, cmd):
        self.dc(0)
        self.cs(0)
        self.spi.write(bytes([cmd]))
        self.cs(1)

    def _write_data(self, data):
        self.dc(1)
        self.cs(0)
        self.spi.write(data if isinstance(data, (bytes, bytearray)) else bytes(data))
        self.cs(1)

    def _write_cmd_data(self, cmd, data):
        self._write_cmd(cmd)
        self._write_data(data)

    def init(self):
        self.rst(0); time.sleep_ms(10)
        self.rst(1); time.sleep_ms(120)
        self._write_cmd(_SWRESET); time.sleep_ms(120)
        self._write_cmd(_SLPOUT);  time.sleep_ms(120)
        self._write_cmd_data(_COLMOD, b'\x05')           # 16-bit color
        self._write_cmd_data(_MADCTL, b'\x00')           # row/col addressing
        self._write_cmd(_DISPON)

    def _set_window(self, x0, y0, x1, y1):
        self._write_cmd(_CASET)
        self._write_data(ustruct.pack(">HH", x0, x1))
        self._write_cmd(_RASET)
        self._write_data(ustruct.pack(">HH", y0, y1))
        self._write_cmd(_RAMWR)

    def fill(self, color):
        self._set_window(0, 0, self.width - 1, self.height - 1)
        chunk = ustruct.pack(">H", color) * 64
        total = self.width * self.height
        self.dc(1); self.cs(0)
        for _ in range(total // 64):
            self.spi.write(chunk)
        remainder = total % 64
        if remainder:
            self.spi.write(ustruct.pack(">H", color) * remainder)
        self.cs(1)

    def pixel(self, x, y, color):
        self._set_window(x, y, x, y)
        self._write_data(ustruct.pack(">H", color))

    def fill_rect(self, x, y, w, h, color):
        self._set_window(x, y, x + w - 1, y + h - 1)
        chunk = ustruct.pack(">H", color) * 32
        total = w * h
        self.dc(1); self.cs(0)
        for _ in range(total // 32):
            self.spi.write(chunk)
        remainder = total % 32
        if remainder:
            self.spi.write(ustruct.pack(">H", color) * remainder)
        self.cs(1)

    def rect(self, x, y, w, h, color):
        self.hline(x,         y,         w, color)
        self.hline(x,         y + h - 1, w, color)
        self.vline(x,         y,         h, color)
        self.vline(x + w - 1, y,         h, color)

    def hline(self, x, y, w, color):
        self.fill_rect(x, y, w, 1, color)

    def vline(self, x, y, h, color):
        self.fill_rect(x, y, 1, h, color)

    def char(self, char, x, y, color, bg=0x0000, size=1):
        code = ord(char) - 32
        if code < 0 or code >= len(_FONT):
            return
        glyph = _FONT[code]
        for col_idx in range(5):
            col_byte = glyph[col_idx]
            for row_idx in range(8):
                px = x + col_idx * size
                py = y + row_idx * size
                if col_byte & (1 << row_idx):
                    if size == 1:
                        self.pixel(px, py, color)
                    else:
                        self.fill_rect(px, py, size, size, color)

    def text(self, string, x, y, color, bg=0x0000, size=1):
        cx = x
        for ch in string:
            self.char(ch, cx, y, color, bg, size)
            cx += (5 + 1) * size
            if cx >= self.width:
                break
