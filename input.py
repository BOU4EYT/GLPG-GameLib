# glpg/input.py — keyboard and mouse input

import pygame as pg
from . import _state


# ── key name → pygame constant map ──────────────────────────────────────────

_KEY_MAP: dict[str, int] = {
    # Letters
    **{k: getattr(pg, f"K_{k}") for k in "abcdefghijklmnopqrstuvwxyz"},
    # Digits
    **{str(n): getattr(pg, f"K_{n}") for n in range(10)},
    # Special keys
    "space":     pg.K_SPACE,
    "enter":     pg.K_RETURN,
    "return":    pg.K_RETURN,
    "escape":    pg.K_ESCAPE,
    "esc":       pg.K_ESCAPE,
    "backspace": pg.K_BACKSPACE,
    "tab":       pg.K_TAB,
    "delete":    pg.K_DELETE,
    "insert":    pg.K_INSERT,
    "home":      pg.K_HOME,
    "end":       pg.K_END,
    "pageup":    pg.K_PAGEUP,
    "pagedown":  pg.K_PAGEDOWN,
    # Arrows
    "up":    pg.K_UP,
    "down":  pg.K_DOWN,
    "left":  pg.K_LEFT,
    "right": pg.K_RIGHT,
    # Modifiers (both sides)
    "shift":  pg.K_LSHIFT,
    "lshift": pg.K_LSHIFT,
    "rshift": pg.K_RSHIFT,
    "ctrl":   pg.K_LCTRL,
    "lctrl":  pg.K_LCTRL,
    "rctrl":  pg.K_RCTRL,
    "alt":    pg.K_LALT,
    "lalt":   pg.K_LALT,
    "ralt":   pg.K_RALT,
    # Function keys
    **{f"f{n}": getattr(pg, f"K_F{n}") for n in range(1, 13)},
}

_MOUSE_MAP: dict[str, int] = {
    "left":   1,
    "middle": 2,
    "right":  3,
}


# ── internal event processor (called by loop each frame) ────────────────────

def _process_events():
    """Read all queued pygame events and update _state input sets."""
    _state._keys_pressed  = set()
    _state._keys_released = set()
    _state._mouse_clicked = set()
    _state._mouse_pos     = pg.mouse.get_pos()

    pressed_buttons = pg.mouse.get_pressed(num_buttons=3)
    _state._mouse_held = {
        btn for btn, held in zip([1, 2, 3], pressed_buttons) if held
    }

    for event in pg.event.get():
        if event.type == pg.QUIT:
            _state.running = False

        elif event.type == pg.KEYDOWN:
            _state._keys_pressed.add(event.key)
            _state._keys_held.add(event.key)

        elif event.type == pg.KEYUP:
            _state._keys_released.add(event.key)
            _state._keys_held.discard(event.key)

        elif event.type == pg.MOUSEBUTTONDOWN:
            _state._mouse_clicked.add(event.button)


# ── key helpers ──────────────────────────────────────────────────────────────

def _resolve_key(k) -> int:
    if isinstance(k, int):
        return k
    k_low = k.lower()
    if k_low in _KEY_MAP:
        return _KEY_MAP[k_low]
    attr = f"K_{k_low}"
    if hasattr(pg, attr):
        return getattr(pg, attr)
    raise ValueError(
        f"Unknown key: '{k}'. Use a letter, digit, or a name like "
        "'space', 'enter', 'up', 'shift', 'f1', etc."
    )


def key(k) -> bool:
    """True every frame the key is held down.

    Example:
        if gl.key("W"): player.move_up()
    """
    return _resolve_key(k) in _state._keys_held


def key_pressed(k) -> bool:
    """True only on the first frame the key is pressed (not held).

    Example:
        if gl.key_pressed("space"): player.jump()
    """
    return _resolve_key(k) in _state._keys_pressed


def key_released(k) -> bool:
    """True only on the frame the key is released.

    Example:
        if gl.key_released("shift"): player.stop_sprint()
    """
    return _resolve_key(k) in _state._keys_released


# ── mouse ────────────────────────────────────────────────────────────────────

class _Mouse:
    """Mouse position and button state.

    Example:
        gl.mouse.pos          # (x, y)
        gl.mouse.x            # x only
        gl.mouse.clicked()    # left click this frame
        gl.mouse.held("right")
    """

    @property
    def pos(self) -> tuple[int, int]:
        """Current (x, y) cursor position."""
        return _state._mouse_pos

    @property
    def x(self) -> int:
        return _state._mouse_pos[0]

    @property
    def y(self) -> int:
        return _state._mouse_pos[1]

    def clicked(self, button: str = "left") -> bool:
        """True only on the frame the button is clicked."""
        btn = _MOUSE_MAP.get(button.lower())
        if btn is None:
            raise ValueError(f"Unknown mouse button: '{button}'. Use 'left', 'right', or 'middle'.")
        return btn in _state._mouse_clicked

    def held(self, button: str = "left") -> bool:
        """True every frame the button is held down."""
        btn = _MOUSE_MAP.get(button.lower())
        if btn is None:
            raise ValueError(f"Unknown mouse button: '{button}'. Use 'left', 'right', or 'middle'.")
        return btn in _state._mouse_held


mouse = _Mouse()
