// Copyright 2026 cornelious
// SPDX-License-Identifier: GPL-2.0-or-later
//
// Shared matrix scanner for every Cornelious board.
//
// All boards present the SAME logical matrix to QMK and Vial: 4 rows x 12 cols,
// the matrix of the Pilot W-Corne (board B), which is the layout's source of truth.
// That is what makes one .vil file load on every board.
//
// Each board only describes its own wiring in its config.h:
//   CORNELIOUS_ROW_PINS        pins driven low one at a time (diode cathode side, COL2ROW)
//   CORNELIOUS_COL_PINS        pins read with pull-ups (diode anode side)
//   CORNELIOUS_PHYS_TO_LOGICAL [rows][cols] table: which logical key, LK(row, col),
//                              sits at each physical row/col crossing, or XX for none.

#include "quantum.h"
#include "matrix.h"

#if !defined(CORNELIOUS_ROW_PINS) || !defined(CORNELIOUS_COL_PINS) || !defined(CORNELIOUS_PHYS_TO_LOGICAL)
#    error "Board config.h must define CORNELIOUS_ROW_PINS, CORNELIOUS_COL_PINS and CORNELIOUS_PHYS_TO_LOGICAL"
#endif

#define LK(r, c) ((uint8_t)(((r) << 4) | (c)))
#define XX 0xFF

static const pin_t row_pins[] = CORNELIOUS_ROW_PINS;
static const pin_t col_pins[] = CORNELIOUS_COL_PINS;

#define PHYS_ROWS (sizeof(row_pins) / sizeof(row_pins[0]))
#define PHYS_COLS (sizeof(col_pins) / sizeof(col_pins[0]))

static const uint8_t phys_to_logical[PHYS_ROWS][PHYS_COLS] = CORNELIOUS_PHYS_TO_LOGICAL;

void matrix_init_custom(void) {
    for (uint8_t r = 0; r < PHYS_ROWS; r++) {
        gpio_set_pin_input_high(row_pins[r]);
    }
    for (uint8_t c = 0; c < PHYS_COLS; c++) {
        gpio_set_pin_input_high(col_pins[c]);
    }
}

bool matrix_scan_custom(matrix_row_t current_matrix[]) {
    matrix_row_t next[MATRIX_ROWS] = {0};

    for (uint8_t r = 0; r < PHYS_ROWS; r++) {
        gpio_set_pin_output(row_pins[r]);
        gpio_write_pin_low(row_pins[r]);
        matrix_output_select_delay();

        for (uint8_t c = 0; c < PHYS_COLS; c++) {
            uint8_t lk = phys_to_logical[r][c];
            if (lk == XX) continue;
            if (!gpio_read_pin(col_pins[c])) {
                next[lk >> 4] |= (MATRIX_ROW_SHIFTER << (lk & 0x0F));
            }
        }

        gpio_set_pin_input_high(row_pins[r]);
        matrix_output_unselect_delay(r, false);
    }

    if (memcmp(current_matrix, next, sizeof(next)) == 0) {
        return false;
    }
    memcpy(current_matrix, next, sizeof(next));
    return true;
}
