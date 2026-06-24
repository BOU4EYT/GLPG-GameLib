# glpg/window.py — display initialisation

import pygame as pg
from . import _state
from . import _color as _c


SIZES = {
    "480p":  (854,  480),
    "720p":  (1280, 720),
    "1080p": (1920, 1080),
    "1440p": (2560, 1440),
}


def window(size="720p", title="GLPG", icon=None, fps=60, bg_color=(0, 0, 0)):
    """
    Initialise the game window.  Call this once before anything else.

    Args:
        size      : Resolution string "480p" | "720p" | "1080p" | "1440p"
                    or a custom (width, height) tuple.
        title     : Window title bar string.
        icon      : Path to an image file to use as the window icon (optional).
        fps       : Target frames per second (default 60).
        bg_color  : Background clear colour — name, hex, or RGB tuple.

    Example:
        gl.window("1080p", title="My Game", fps=144, bg_color="#1a1a2e")
    """
    if not pg.get_init():
        pg.init()

    # ── resolve resolution ──────────────────────────────────────────────────
    if isinstance(size, str):
        resolution = SIZES.get(size.lower())
        if resolution is None:
            raise ValueError(
                f"Unknown size string '{size}'. "
                f"Choose from {list(SIZES.keys())} or pass a (w, h) tuple."
            )
    elif isinstance(size, (tuple, list)) and len(size) == 2:
        resolution = (int(size[0]), int(size[1]))
    else:
        raise TypeError(f"size must be a resolution string or (w, h) tuple, got: {size!r}")

    # ── create display ──────────────────────────────────────────────────────
    _state.screen   = pg.display.set_mode(resolution)
    _state.clock    = pg.time.Clock()
    _state.fps      = fps
    _state.bg_color = _c.parse(bg_color)

    pg.display.set_caption(title)

    if icon:
        try:
            icon_surf = pg.image.load(icon).convert_alpha()
            pg.display.set_icon(icon_surf)
        except pg.error as e:
            raise FileNotFoundError(f"Could not load icon '{icon}': {e}")


# ── helpers ─────────────────────────────────────────────────────────────────

def get_screen():
    """Return the raw pygame Surface."""
    return _state.screen


def get_size():
    """Return (width, height) of the current window."""
    if _state.screen:
        return _state.screen.get_size()
    raise RuntimeError("Window not initialised — call gl.window() first.")


def get_width():
    return get_size()[0]


def get_height():
    return get_size()[1]


def set_title(title: str):
    """Update the window title bar text."""
    pg.display.set_caption(title)


def set_fps(fps: int):
    """Change the target FPS cap."""
    _state.fps = fps


def set_bg_color(color):
    """Change the background clear colour."""
    _state.bg_color = _c.parse(color)
