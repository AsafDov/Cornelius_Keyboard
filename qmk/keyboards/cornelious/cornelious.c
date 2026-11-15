// Copyright 2026 cornelious
// SPDX-License-Identifier: GPL-2.0-or-later
//
// Shared by every Cornelious board.
//
// Alt+Tab that behaves like holding a real Alt key. When an Alt+Tab key
// (LALT(KC_TAB) or RALT(KC_TAB) in Vial) is on a layer you are holding, Alt
// stays down after the first tap, so each further tap steps through the
// window switcher. Letting go of the layer key releases Alt, which switches
// to the selected window. While the switcher is open, the arrow keys move
// through it and Esc closes it; any other key releases Alt first.
// On the base layer the key is an ordinary Alt+Tab.
//
// It also answers VIA's "jump to bootloader" command, which Vial drops from
// insecure builds, so `scripts/vial_tool.py bootloader` can start a flash
// without anyone touching the board.

#include "quantum.h"
#ifdef VIA_ENABLE
#    include "via.h"
#endif

static uint16_t bootloader_requested_at = 0;
static bool     bootloader_requested    = false;

#define NO_LAYER 0xFF

static uint8_t alt_tab_layer    = NO_LAYER; // layer holding Alt down, or NO_LAYER
static bool    alt_tab_tab_down = false;

static bool is_alt_tab(uint16_t keycode) {
    return keycode == LALT(KC_TAB) || keycode == RALT(KC_TAB);
}

static bool keeps_switcher_open(uint16_t keycode) {
    switch (keycode) {
        case KC_LEFT:
        case KC_RGHT:
        case KC_UP:
        case KC_DOWN:
        case KC_ESC:
            return true;
        default:
            return is_alt_tab(keycode);
    }
}

static void alt_tab_release(void) {
    if (alt_tab_layer != NO_LAYER) {
        unregister_mods(MOD_BIT(KC_LALT));
        alt_tab_layer = NO_LAYER;
    }
}

bool process_record_kb(uint16_t keycode, keyrecord_t *record) {
    if (record->event.pressed && alt_tab_layer != NO_LAYER && !keeps_switcher_open(keycode)) {
        alt_tab_release();
    }

    if (is_alt_tab(keycode)) {
        if (record->event.pressed) {
            uint8_t layer = layer_switch_get_layer(record->event.key);
            if (layer != get_highest_layer(default_layer_state)) {
                if (alt_tab_layer == NO_LAYER) {
                    register_mods(MOD_BIT(KC_LALT)); // left Alt: right Alt is AltGr on some layouts
                    alt_tab_layer = layer;
                }
                register_code(KC_TAB); // held like a real Tab, so holding it auto-repeats
                alt_tab_tab_down = true;
                return false;
            }
        } else if (alt_tab_tab_down) {
            unregister_code(KC_TAB);
            alt_tab_tab_down = false;
            return false;
        }
    }

    return process_record_user(keycode, record);
}

#ifdef VIA_ENABLE
// Only reached for commands via.c doesn't handle itself. Secure Vial builds
// handle the bootloader jump there (and only while unlocked); insecure builds
// pass it on to here.
void raw_hid_receive_kb(uint8_t *data, uint8_t length) {
    if (data[0] == id_bootloader_jump) {
        // jump a moment later, so the reply reaches the PC first
        bootloader_requested    = true;
        bootloader_requested_at = timer_read();
        return; // reply echoes the command: handled
    }
    data[0] = id_unhandled;
}
#endif

void housekeeping_task_kb(void) {
    // the layer key was released (or the layer toggled off): finish the switch
    if (alt_tab_layer != NO_LAYER && !layer_state_is(alt_tab_layer)) {
        alt_tab_release();
    }
    if (bootloader_requested && timer_elapsed(bootloader_requested_at) > 100) {
        bootloader_jump();
    }
    housekeeping_task_user();
}
