# glpg/__init__.py — public API
"""
GLPG — GameLib for Pygame
A shorthand wrapper that makes pygame fast and approachable.

MIT License 2026

Quickstart (managed loop):
    import glpg as gl

    gl.window("720p", title="My Game")

    @gl.on_update
    def update(dt):
        if gl.key("escape"):
            gl.quit()

    @gl.on_draw
    def draw():
        gl.draw.rect(100, 100, 64, 64, "#e63946")
        gl.draw.text("Hello GLPG", 20, 20, size=32, color="white")

    gl.run()

Quickstart (manual loop):
    import glpg as gl

    gl.window("720p", title="My Game")

    while (dt := gl.tick()) is not None:
        if gl.key("escape"):
            gl.quit()
        gl.draw.rect(100, 100, 64, 64, "red")
        gl.flip()
"""

import pygame as _pg

# ── window ────────────────────────────────────────────────────────────────
from .window import (
    window,
    get_screen,
    get_size,
    get_width,
    get_height,
    set_title,
    set_fps,
    set_bg_color,
)

# ── loop ──────────────────────────────────────────────────────────────────
from .loop import (
    on_update,
    on_draw,
    run,
    tick,
    flip,
    quit,
    is_running,
    get_fps,
)

# ── input ─────────────────────────────────────────────────────────────────
from .input import key, key_pressed, key_released, mouse

# ── draw (namespace) ──────────────────────────────────────────────────────
from . import draw

# ── meta ──────────────────────────────────────────────────────────────────
__version__ = "1.0.0"
__author__  = "GLPG"
__license__ = "MIT"
