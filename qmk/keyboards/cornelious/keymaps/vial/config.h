// Copyright 2026 cornelious
// SPDX-License-Identifier: GPL-2.0-or-later

#pragma once

// Same UID as the Pilot W-Corne (board B). Vial treats every Cornelious board
// as the same keyboard, so one .vil file loads on all of them without warnings.
#define VIAL_KEYBOARD_UID { 0xF7, 0x47, 0x28, 0xAF, 0x31, 0xF6, 0x2F, 0x36 }

// No unlock combo: rules.mk builds Vial in insecure mode (always unlocked).

// Match board B's capacity, so a .vil from any board fits on every board.
#define DYNAMIC_KEYMAP_LAYER_COUNT 8
#define DYNAMIC_KEYMAP_MACRO_COUNT 16
#define VIAL_TAP_DANCE_ENTRIES 32
#define VIAL_COMBO_ENTRIES 32
#define VIAL_KEY_OVERRIDE_ENTRIES 32

// Vial "QMK Settings" from layout/cornelious.vil (generated).
#include "layout_settings.h"
