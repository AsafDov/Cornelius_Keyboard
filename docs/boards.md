# Boards

## B: Pilot W-Corne (layout source of truth)

- USB: VID `0x55D4`, PID `0x0461`, manufacturer "Pilot", product "W-CORNE"
- Vial protocol 6, VIA protocol 9, UID `f74728af31f62f36`
- 46 keys: 3x6 + 3 thumbs per half, plus 2 extra keys in the inner column of each half
- Logical matrix 4 rows x 12 cols (see the README for which key is which)
- 8 layers, 16 macros, 32 tap dances, 32 combos, 32 key overrides
- Firmware: vendor build; source not available. Not built from this repo.
- Its Vial definition as read from the firmware: `layout/w-corne-vial.json`

## A: Cornelius V1, `rp2040zero` (handwired)

- Controller: **Waveshare RP2040-Zero** (RP2040, 2 MB flash), with an onboard WS2812 LED on GP16 (unused)
- **One controller for both halves.** No split link, no handedness setting. Each
  half's switches run straight to the controller's pins (4 rows + 6 columns per half,
  all 20 edge GPIOs used).
- 42 keys: 3x6 + 3 thumbs per half (no extra inner keys)
- Diodes: COL2ROW (rows driven low, columns read with pull-ups)

| Half | Row pins (top -> thumbs) | Column pins |
| --- | --- | --- |
| Left | GP15, GP14, GP13, GP12 | GP1, GP0, GP29, GP28, GP27, GP26 (outer pinky -> inner) |
| Right | GP8, GP9, GP10, GP11 | GP7, GP6, GP5, GP2, GP3, GP4 (inner -> outer pinky) |

Thumb rows use only 3 columns: left GP28, GP27, GP26 (outer -> inner), right GP7,
GP6, GP5 (inner -> outer). The outer pinky column of the right half is GP4.

- USB on QMK: VID `0xFEED`, PID `0xC0E1`, "Cornelious RP2040-Zero"
- Bootloader: hold BOOT + tap RESET, or double-tap RESET (QMK)
- History: ran KMK via Pog (CircuitPython 9.2.0) until 2026-11-15, then Vial-QMK
  from this repo. The KMK files are on the `kmk` branch (tag `kmk-final`).
