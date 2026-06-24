# glpg/_state.py — internal shared state across all modules

import pygame as pg

# Display
screen = None
clock  = None
fps    = 60
bg_color = (0, 0, 0)

# Loop
running = False

# Input — reset/updated every frame by input._process_events()
_events         = []
_keys_pressed   = set()   # fired only on first-frame press
_keys_released  = set()   # fired only on release frame
_keys_held      = set()   # true for every frame the key is down
_mouse_clicked  = set()   # fired only on click frame
_mouse_held     = set()   # true for every frame button is down
_mouse_pos      = (0, 0)
