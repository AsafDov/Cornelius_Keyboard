// Copyright 2026 cornelious
// SPDX-License-Identifier: GPL-2.0-or-later
//
// The RP2040-Zero's onboard RGB LED (GP16) shows the active layer.
// Brightness is NOT set here: it is whatever the Vial Lighting tab says
// (default 36/255, capped at 40/255 in keyboard.json).
// Green looks strong on this LED, so orange needs a low hue and high saturation
// to look orange rather than yellow.

#include "quantum.h"

// { hue, saturation } on QMK's 0-255 scale
static const uint8_t layer_colour[][2] = {
    [0] = {110, 180}, // base:    teal leaning green
    [1] = {12, 235},  // nav:     orange
    [2] = {38, 220},  // symbols: yellow (a touch of extra red so it doesn't look green)
};
#define OTHER_LAYER_COLOUR {191, 120} // any other layer: soft lavender

static void show_layer_colour(layer_state_t state) {
    uint8_t layer     = get_highest_layer(state | default_layer_state);
    uint8_t colour[2] = OTHER_LAYER_COLOUR;
    if (layer < ARRAY_SIZE(layer_colour)) {
        colour[0] = layer_colour[layer][0];
        colour[1] = layer_colour[layer][1];
    }
    // keeps the current brightness; does nothing while the LED is switched off in Vial
    rgblight_sethsv_noeeprom(colour[0], colour[1], rgblight_get_val());
}

layer_state_t layer_state_set_kb(layer_state_t state) {
    state = layer_state_set_user(state);
    show_layer_colour(state);
    return state;
}

void keyboard_post_init_kb(void) {
    show_layer_colour(layer_state);
    keyboard_post_init_user();
}
