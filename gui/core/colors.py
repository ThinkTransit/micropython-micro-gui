# colors.py Micropython GUI library for TFT displays: colors and shapes

# Released under the MIT License (MIT). See LICENSE.
# Copyright (c) 2019 Peter Hinch
from hardware_setup import SSD

# Code can be portable between 4-bit and other drivers by calling create_color
def create_color(idx, r, g, b):
    c = SSD.rgb(r, g, b)
    if not hasattr(SSD, 'lut'):
        return c
    if not 0 <= idx <= 15:
        raise ValueError('Color nos must be 0..15')
    x = idx << 1
    SSD.lut[x] = c & 0xff
    SSD.lut[x + 1] = c >> 8
    return idx

if hasattr(SSD, 'lut'):  # Colors defined by LUT
    BLACK = create_color(0, 0, 0, 0)
    GREEN = create_color(1, 0, 255, 0)
    RED = create_color(2, 255, 0, 0)
    LIGHTRED = create_color(3, 140, 0, 0)
    BLUE = create_color(4, 0, 0, 255)
    YELLOW = create_color(5, 255, 255, 0)
    GREY = create_color(6, 100, 100, 100)
    MAGENTA = create_color(7, 255, 0, 255)
    CYAN = create_color(8, 0, 255, 255)
    LIGHTGREEN = create_color(9, 0, 100, 0)
    DARKGREEN = create_color(10, 0, 80, 0)
    DARKBLUE = create_color(11, 0, 0, 90)
    # 12, 13, 14 free for user definition
    WHITE = create_color(15, 255, 255, 255)
else:
    BLACK = SSD.rgb(0, 0, 0)
    GREEN = SSD.rgb(0, 255, 0)
    RED = SSD.rgb(255, 0, 0)
    LIGHTRED = SSD.rgb(140, 0, 0)
    BLUE = SSD.rgb(0, 0, 255)
    YELLOW = SSD.rgb(255, 255, 0)
    GREY = SSD.rgb(100, 100, 100)
    MAGENTA = SSD.rgb(255, 0, 255)
    CYAN = SSD.rgb(0, 255, 255)
    LIGHTGREEN = SSD.rgb(0, 100, 0)
    DARKGREEN = SSD.rgb(0, 80, 0)
    DARKBLUE = SSD.rgb(0, 0, 90)
    WHITE = SSD.rgb(255, 255, 255)

# Color used when clearing the screen
BGCOLOR = BLACK

# RA8875 defines colors as 3-tuples with greying-out operating on those.
# Should we assign GREY to any color > 0?
CIRCLE = 1
RECTANGLE = 2
CLIPPED_RECT = 3