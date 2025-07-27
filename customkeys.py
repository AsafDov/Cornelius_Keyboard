# These are yous custom keycodes do any needed imports at the top - v1.0.0
# then you can reference them in your keymap with for example customkeys.MyKey

from kmk.keys import KC
from kmk.modules.macros import Tap, Release, Press

MyKey = KC.X
ALT_BSPC = KC.HT(KC.BSPC, KC.LALT)
SHFT_TAB = KC.HT(KC.TAB, KC.LSFT)
NAV_SPC = KC.HT(KC.SPC,KC.MO(1))
LCTRL_ENT = KC.HT(KC.ENT,KC.LCTRL)
LSFT_ENT = KC.HT(KC.ENT,KC.LSFT)
WIN_LCTRL =KC.HT(KC.LALT(KC.SPC), KC.LCTL)
SYM_SPC = KC.HT(KC.SPC,KC.MO(2))
LEFT_WORD = KC.LCTRL(KC.LEFT)
RIGHT_WORD = KC.LCTRL(KC.RIGHT)
SELECT_LEFT = KC.LSFT(KC.LEFT)
SELECT_RIGHT = KC.LSFT(KC.RIGHT)
SELECT_RIGHT_WORD = KC.LCTRL(KC.LSFT(KC.RIGHT))
SELECT_LEFT_WORD = KC.LCTRL(KC.LSFT(KC.LEFT))
DEL_LEFT_WORD = KC.LCTRL(KC.BSPC)
DEL_RIGHT_WORD = KC.LCTRL(KC.DEL)
COPY = KC.LCTRL(KC.C)
CUT = KC.LCTRL(KC.X)
UNDO = KC.LCTRL(KC.Z)
REDO = KC.LCTRL(KC.Y)
PASTE = KC.LCTRL(KC.V)
COMMENT = KC.LCTRL(KC.SLSH)
MOUSE_SHFT = KC.HT(KC.TG(3),KC.LSFT)
SYM_SHFT = KC.HT(KC.TG(2),KC.LSFT)

MOUSE_UP = KC.MS_UP
MOUSE_DOWN = KC.MS_DOWN
MOUSE_LEFT = KC.MS_LEFT
MOUSE_RIGHT = KC.MS_RIGHT
MOUSE_PAN_LEFT = KC.MW_LEFT
MOUSE_PAN_RIGHT = KC.MW_RIGHT
MOUSE_LEFT_CLK = KC.MB_LMB
MOUSE_RIGHT_CLK = KC.MB_RMB
MOUSE_MID_CLK = KC.MB_MMB
SCROLL_UP = KC.MW_UP
SCROLL_DOWN = KC.MW_DOWN
LANGUAGE = KC.LALT(KC.LSFT)
CLIPBOARD = KC.LGUI(KC.V)
RTL = KC.RCTRL(KC.RSFT)
NEXT_TAB = KC.LCTRL(KC.TAB)
PREV_TAB = KC.LCTRL(KC.LSFT(KC.TAB))

# KC.MB_LMB	Left mouse button
# KC.MB_RMB	Right mouse button
# KC.MB_MMB	Middle mouse button
# KC.MB_BTN4	mouse button 4
# KC.MB_BTN5	mouse button 5
# KC.MW_UP	Mouse wheel up
# KC.MW_DOWN, KC.MW_DN	Mouse wheel down
# KC.MW_LEFT, KC.MW_LT	Mouse pan left
# KC.MW_RIGHT, KC.MW_RT	Mouse pan right
# KC.MS_UP	Move mouse cursor up
# KC.MS_DOWN, KC.MS_DN	Move mouse cursor down
# KC.MS_LEFT, KC.MS_LT	Move mouse cursor left
# KC.MS_RIGHT, KC.MS_RT	Move mouse cursor right


def next_boot_dfu(keyboard):
    print('setting next boot to dfu') #serial feedback
    import microcontroller
    microcontroller.on_next_reset(microcontroller.RunMode.UF2)

DFUMODE = KC.MACRO(next_boot_dfu)

def next_boot_safe(keyboard):
    print('setting next boot to safe') #serial feedback
    import microcontroller
    microcontroller.on_next_reset(microcontroller.RunMode.SAFE_MODE)
SAFEMODE = KC.MACRO(next_boot_safe)

def toggle_drive(keyboard):
    print('toggling usb drive') #serial feedback
    import microcontroller
    if microcontroller.nvm[0] == 0:
        microcontroller.nvm[0] = 1
    else:
        microcontroller.nvm[0] = 0

ToggleDrive = KC.MACRO(toggle_drive)