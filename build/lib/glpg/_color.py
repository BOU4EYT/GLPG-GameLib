# glpg/_color.py — universal color parser

import pygame as pg


def parse(color):
    """
    Accept any of:
      - RGB / RGBA tuple  → (255, 0, 0) | (255, 0, 0, 128)
      - Hex string        → "#ff0000"   | "#ff0000ff"
      - Named string      → "red"  "white"  "cornflowerblue"  etc.
    Returns an (R, G, B) or (R, G, B, A) tuple.
    """
    if isinstance(color, (tuple, list)):
        if len(color) in (3, 4):
            return tuple(int(c) for c in color)
        raise ValueError(f"Color tuple must have 3 or 4 values, got {len(color)}: {color}")

    if isinstance(color, str):
        stripped = color.strip()

        if stripped.startswith("#"):
            h = stripped.lstrip("#")
            if len(h) == 6:
                return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))
            if len(h) == 8:
                return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), int(h[6:8], 16))
            raise ValueError(f"Invalid hex color: '{color}' — expected #RRGGBB or #RRGGBBAA")

        # Named color — let pygame validate it
        try:
            c = pg.Color(stripped)
            return (c.r, c.g, c.b) if c.a == 255 else (c.r, c.g, c.b, c.a)
        except ValueError:
            raise ValueError(
                f"Unknown color name: '{color}'. "
                "Use a pygame color name, hex string, or RGB tuple."
            )

    raise TypeError(f"Unsupported color type: {type(color).__name__} — value: {color!r}")
