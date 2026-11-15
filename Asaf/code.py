print("Starting")

import board

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.modules.holdtap import HoldTap
from kmk.modules.layers import Layers
holdtap = HoldTap()
# optional: set a custom tap timeout in ms
# holdtap.tap_time = 300

keyboard = KMKKeyboard()
keyboard.modules.append(holdtap)
keyboard.modules.append(Layers())

keyboard.col_pins = (board.GP1,board.GP0,board.GP29,board.GP28,board.GP27,board.GP26,board.GP7,board.GP6,board.GP5,board.GP2,board.GP3,board.GP4)
keyboard.row_pins = (board.GP15,board.GP14,board.GP13,board.GP12,board.GP11,board.GP10,board.GP9,board.GP8,)
keyboard.diode_orientation = DiodeOrientation.COL2ROW
rollover_cols_every_rows = 4

keyboard.coord_mapping = \
    [
        0 , 1, 2, 3, 4, 5,      90,91,92,93,94,95,
        12,13,14,15,16,17,      78,79,80,81,82,83,
        24,25,26,27,28,29,      66,67,68,69,70,71,
                 39,40,41,      54,55,56,

    ]

ALT_BSPC = KC.HT(KC.BSPC, KC.LALT)
SHFT_CAPSLOCK = KC.HT(KC.CAPS, KC.LSFT)
NAV_SPC = KC.HT(KC.SPC,KC.MO(1))
WIN_LCTRL =KC.HT(KC.LGUI, KC.LCTL)
SYM_SPC = KC.HT(KC.SPC,KC.MO(2))

keyboard.keymap = [

    [
        #BASE
        KC.TAB,KC.Q,KC.W,KC.E,KC.R,KC.T,          KC.Y,KC.U,KC.I,KC.O,KC.P,KC.N6, #ROW 1 |12
        SHFT_CAPSLOCK,KC.A,KC.S,KC.D,KC.F,KC.G,   KC.H,KC.J,KC.K,KC.L,KC.SCLN,KC.QUOT, #ROW 2 | 12
        WIN_LCTRL,KC.Z,KC.X,KC.C,KC.V,KC.B,         KC.N,KC.M,KC.COMMA,KC.DOT,KC.SLSH,KC.GRV, #ROW 3 | 12
                ALT_BSPC,NAV_SPC,KC.ENT,           KC.ENT,KC.HT(KC.SPC,KC.MO(2)),KC.NO, #ROW 4 |12
    ],
    [
        #NAV
        KC.A,KC.B,KC.C,KC.D,KC.E,KC.H,          KC.NO,KC.NO,KC.UP,KC.NO,KC.NO,KC.NO, #ROW 1 |12
        KC.N0,KC.N1,KC.N1,KC.N1,KC.N1,KC.N3,    KC.LCTL(KC.LEFT),KC.LEFT,KC.DOWN,KC.RGHT,KC.LCTL(KC.RGHT),KC.NO, #ROW 2 | 12
        KC.N0,KC.N1,KC.N1,KC.N1,KC.N1,KC.N3,    KC.NO,KC.LSFT(KC.LEFT),KC.NO,KC.LSFT(KC.RIGHT),KC.NO,KC.NO, #ROW 3 | 12
        KC.NO,KC.NO,KC.NO,KC.N0,KC.N1,KC.N2,    KC.NO,KC.NO,KC.NO,KC.NO,KC.NO,KC.NO, #ROW 4 |12
    ],

    [
        #SYMBOLS
        KC.TAB,KC.N1,KC.N2,KC.LPRN,KC.RPRN,KC.N5,          KC.N6,KC.N7,KC.N8,KC.N9,KC.MINS,KC.EQL, #ROW 1 |12
        SHFT_CAPSLOCK,KC.A,KC.S,KC.LBRC,KC.RBRC,KC.G,   KC.H,KC.TRNS,KC.K,KC.L,KC.SCLN,KC.QUOT, #ROW 2 | 12
        WIN_LCTRL,KC.Z,KC.X,KC.LCBR,KC.RCBR,KC.B,         KC.N,KC.M,KC.COMMA,KC.DOT,KC.SLSH,KC.GRV, #ROW 3 | 12
                ALT_BSPC,NAV_SPC,KC.ENT,           KC.ENT,KC.SPC,KC.NO, #ROW 4 |12
    ],

]
if __name__ == '__main__':
    keyboard.go()
