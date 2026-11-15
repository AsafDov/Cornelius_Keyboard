// Copyright 2026 cornelious
// SPDX-License-Identifier: GPL-2.0-or-later
//
// Board A (Cornelius V1): handwired 42-key Corne (3x6 + 3 thumbs per half).
// One Waveshare RP2040-Zero drives BOTH halves directly (no split link, no
// handedness). Each half has its own 4 row pins and 6 column pins.
// Diodes are COL2ROW: rows are driven low, columns are read with pull-ups.
// Wiring taken from the board's old KMK/Pog config (pog.json on the kmk branch).
//
//   Left half : rows GP15 (top) GP14 GP13 GP12 (thumbs)
//               cols GP1 GP0 GP29 GP28 GP27 GP26   (outer pinky -> inner)
//   Right half: rows GP8 (top)  GP9  GP10 GP11 (thumbs)
//               cols GP7 GP6 GP5 GP2 GP3 GP4       (inner -> outer pinky)
//
// The 4 extra inner keys of the 46-key W-Corne layout, LK(3,0) LK(3,1)
// LK(0,6) LK(1,6), do not exist on this board.

#pragma once

#define CORNELIOUS_ROW_PINS { GP8, GP9, GP10, GP11, GP12, GP13, GP14, GP15 }
#define CORNELIOUS_COL_PINS { GP2, GP3, GP4, GP5, GP6, GP7, GP26, GP27, GP28, GP29, GP0, GP1 }

// clang-format off
#define CORNELIOUS_PHYS_TO_LOGICAL { \
    /*            GP2        GP3        GP4        GP5       GP6       GP7       GP26      GP27      GP28      GP29      GP0       GP1     */ \
    /* GP8  */ { LK(0,10), LK(0,11), LK(3, 9), LK(0,9),  LK(0,8),  LK(0,7),  XX,       XX,       XX,       XX,       XX,       XX       }, \
    /* GP9  */ { LK(1,10), LK(1,11), LK(3,10), LK(1,9),  LK(1,8),  LK(1,7),  XX,       XX,       XX,       XX,       XX,       XX       }, \
    /* GP10 */ { LK(2,10), LK(2,11), LK(3,11), LK(2,9),  LK(2,8),  LK(2,7),  XX,       XX,       XX,       XX,       XX,       XX       }, \
    /* GP11 */ { XX,       XX,       XX,       LK(3,8),  LK(3,7),  LK(3,6),  XX,       XX,       XX,       XX,       XX,       XX       }, \
    /* GP12 */ { XX,       XX,       XX,       XX,       XX,       XX,       LK(3,5),  LK(3,4),  LK(3,3),  XX,       XX,       XX       }, \
    /* GP13 */ { XX,       XX,       XX,       XX,       XX,       XX,       LK(2,5),  LK(2,4),  LK(2,3),  LK(2,2),  LK(2,1),  LK(2,0)  }, \
    /* GP14 */ { XX,       XX,       XX,       XX,       XX,       XX,       LK(1,5),  LK(1,4),  LK(1,3),  LK(1,2),  LK(1,1),  LK(1,0)  }, \
    /* GP15 */ { XX,       XX,       XX,       XX,       XX,       XX,       LK(0,5),  LK(0,4),  LK(0,3),  LK(0,2),  LK(0,1),  LK(0,0)  }, \
}
// clang-format on

// Double-tap the reset button to enter the UF2 bootloader (the RP2040-Zero's
// BOOT button also works: hold BOOT, tap RESET).
#define RP2040_BOOTLOADER_DOUBLE_TAP_RESET
#define RP2040_BOOTLOADER_DOUBLE_TAP_RESET_TIMEOUT 500U
