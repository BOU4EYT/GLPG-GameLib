# glpg/draw.py — drawing helpers

import pygame as pg
from . import _state
from . import _color as _c


# ── font cache ───────────────────────────────────────────────────────────────

_font_cache: dict[tuple, pg.font.Font] = {}
_image_cache: dict[str, pg.Surface]    = {}


def _font(name: str | None, size: int) -> pg.font.Font:
    key = (name, size)
    if key not in _font_cache:
        if name is None:
            _font_cache[key] = pg.font.SysFont(None, size)
        else:
            try:
                _font_cache[key] = pg.font.SysFont(name, size)
            except Exception:
                _font_cache[key] = pg.font.SysFont(None, size)
    return _font_cache[key]


def _surf() -> pg.Surface:
    if _state.screen is None:
        raise RuntimeError("Call gl.window() before drawing.")
    return _state.screen


# ── shapes ───────────────────────────────────────────────────────────────────

def rect(x, y, w, h, color="white", border: int = 0, radius: int = 0):
    """
    Draw a rectangle.

    Args:
        x, y          : Top-left position.
        w, h          : Width and height.
        color         : Fill colour (name / hex / RGB tuple).
        border        : Line width in pixels; 0 = filled.
        radius        : Corner radius for rounded rectangles.

    Example:
        gl.draw.rect(100, 100, 64, 64, "#e63946")
        gl.draw.rect(100, 100, 64, 64, "white", border=2, radius=8)
    """
    pg.draw.rect(_surf(), _c.parse(color), (x, y, w, h), border, border_radius=radius)


def circle(x, y, radius, color="white", border: int = 0):
    """
    Draw a circle.

    Args:
        x, y    : Centre position.
        radius  : Radius in pixels.
        color   : Colour (name / hex / RGB tuple).
        border  : Line width; 0 = filled.

    Example:
        gl.draw.circle(200, 200, 40, "cyan")
    """
    pg.draw.circle(_surf(), _c.parse(color), (int(x), int(y)), int(radius), border)


def ellipse(x, y, w, h, color="white", border: int = 0):
    """
    Draw an ellipse inside the bounding box (x, y, w, h).

    Example:
        gl.draw.ellipse(100, 100, 200, 80, "yellow")
    """
    pg.draw.ellipse(_surf(), _c.parse(color), (int(x), int(y), int(w), int(h)), border)


def line(x1, y1, x2, y2, color="white", width: int = 1):
    """
    Draw a line from (x1, y1) to (x2, y2).

    Example:
        gl.draw.line(0, 0, 400, 300, "#ff0000", width=3)
    """
    pg.draw.line(_surf(), _c.parse(color), (x1, y1), (x2, y2), max(1, width))


def polygon(points: list[tuple], color="white", border: int = 0):
    """
    Draw a polygon from a list of (x, y) points.

    Example:
        gl.draw.polygon([(100,50), (150,150), (50,150)], "green")
    """
    pg.draw.polygon(_surf(), _c.parse(color), points, border)


# ── text ─────────────────────────────────────────────────────────────────────

def text(
    content,
    x, y,
    size: int = 24,
    color="white",
    font: str | None = None,
    center: bool = False,
    antialias: bool = True,
) -> pg.Rect:
    """
    Draw text at (x, y).

    Args:
        content   : String (or anything str()-able) to render.
        x, y      : Position (top-left unless center=True).
        size      : Font size in points.
        color     : Text colour.
        font      : System font name, or None for the default font.
        center    : If True, the text is centred on (x, y).
        antialias : Smooth edges (default True).

    Returns:
        pygame.Rect of the rendered text.

    Example:
        gl.draw.text("Score: 0", 20, 20, size=32, color="gold")
        gl.draw.text("PAUSED", cx, cy, size=64, color="white", center=True)
    """
    f    = _font(font, size)
    surf = f.render(str(content), antialias, _c.parse(color))
    if center:
        r = surf.get_rect(center=(int(x), int(y)))
    else:
        r = surf.get_rect(topleft=(int(x), int(y)))
    _surf().blit(surf, r)
    return r


# ── image ────────────────────────────────────────────────────────────────────

def image(
    path: str,
    x, y,
    scale: float = 1.0,
    center: bool = False,
    cache: bool = True,
) -> pg.Rect:
    """
    Draw an image from a file path.

    Args:
        path    : Relative or absolute path to the image file.
        x, y    : Position (top-left unless center=True).
        scale   : Scale multiplier (1.0 = original size).
        center  : If True, the image is centred on (x, y).
        cache   : Cache the loaded surface (default True).

    Returns:
        pygame.Rect of the drawn image.

    Example:
        gl.draw.image("assets/player.png", player.x, player.y)
        gl.draw.image("assets/logo.png", cx, cy, scale=0.5, center=True)
    """
    if cache and path in _image_cache:
        surf = _image_cache[path]
    else:
        try:
            surf = pg.image.load(path).convert_alpha()
        except pg.error as e:
            raise FileNotFoundError(f"Could not load image '{path}': {e}")
        if cache:
            _image_cache[path] = surf

    if scale != 1.0:
        w = max(1, int(surf.get_width()  * scale))
        h = max(1, int(surf.get_height() * scale))
        surf = pg.transform.scale(surf, (w, h))

    if center:
        r = surf.get_rect(center=(int(x), int(y)))
    else:
        r = surf.get_rect(topleft=(int(x), int(y)))

    _surf().blit(surf, r)
    return r


def clear_image_cache():
    """Evict all cached image surfaces (useful between scenes)."""
    _image_cache.clear()


# ── surface ──────────────────────────────────────────────────────────────────

def clear(color=None):
    """
    Fill the screen with a solid colour.
    Defaults to the bg_color set in gl.window() if no colour is given.

    Example:
        gl.draw.clear("#0d0d0d")
    """
    _surf().fill(_c.parse(color) if color is not None else _state.bg_color)
