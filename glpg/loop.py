# glpg/loop.py — managed and manual game loop

import pygame as pg
from . import _state
from . import input as _input


# ── registered hooks (managed loop) ─────────────────────────────────────────

_update_fn = None
_draw_fn   = None


def on_update(fn):
    """
    Decorator — register a function to run every frame.
    Receives `dt` (delta-time in seconds since last frame).

    Example:
        @gl.on_update
        def update(dt):
            player.x += speed * dt
    """
    global _update_fn
    _update_fn = fn
    return fn


def on_draw(fn):
    """
    Decorator — register a function to run every frame for rendering.
    Called after the screen is cleared.

    Example:
        @gl.on_draw
        def draw():
            gl.draw.rect(player.x, player.y, 32, 32, "red")
    """
    global _draw_fn
    _draw_fn = fn
    return fn


# ── managed loop ─────────────────────────────────────────────────────────────

def run():
    """
    Start the managed game loop.  Blocks until the window is closed.
    Requires gl.window() to have been called first.
    Register logic with @gl.on_update and rendering with @gl.on_draw.

    Example:
        gl.window("720p", title="My Game")

        @gl.on_update
        def update(dt): ...

        @gl.on_draw
        def draw(): ...

        gl.run()
    """
    _require_window("gl.run()")
    _state.running = True

    while _state.running:
        dt = _state.clock.tick(_state.fps) / 1000.0
        _input._process_events()

        if not _state.running:
            break

        _state.screen.fill(_state.bg_color)

        if _update_fn:
            _update_fn(dt)
        if _draw_fn:
            _draw_fn()

        pg.display.flip()

    pg.quit()


# ── manual loop ──────────────────────────────────────────────────────────────

def tick() -> float | None:
    """
    Manual loop mode — call once at the top of your own while loop.
    Handles events, clears the screen, and returns dt in seconds.
    Returns None (and calls pg.quit) when the window should close.

    Example:
        gl.window("720p")
        while (dt := gl.tick()) is not None:
            if gl.key("escape"):
                gl.quit()
            gl.draw.rect(x, y, 32, 32, "white")
            gl.flip()
    """
    _require_window("gl.tick()")

    if not _state.running:
        _state.running = True

    dt = _state.clock.tick(_state.fps) / 1000.0
    _input._process_events()

    if not _state.running:
        pg.quit()
        return None

    _state.screen.fill(_state.bg_color)
    return dt


def flip():
    """
    Manual loop mode — push the current frame to the display.
    Call once at the end of your loop body.
    """
    pg.display.flip()


# ── shared utilities ─────────────────────────────────────────────────────────

def quit():
    """Signal the loop to stop at the end of the current frame."""
    _state.running = False


def is_running() -> bool:
    """True while the game loop is active."""
    return _state.running


def get_fps() -> float:
    """Return the actual measured FPS this frame."""
    if _state.clock:
        return _state.clock.get_fps()
    return 0.0


# ── internal ─────────────────────────────────────────────────────────────────

def _require_window(caller: str):
    if _state.screen is None:
        raise RuntimeError(f"Call gl.window() before {caller}.")
