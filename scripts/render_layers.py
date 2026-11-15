#!/usr/bin/env python3
"""Draw every layer of layout/cornelious.vil as a PNG, exactly as Vial shows it.

Uses vial-gui's own keyboard widget (rendered off-screen), so the pictures match
the Vial app. Output: docs/layers/layer-<n>.png for every layer that isn't
completely transparent. Rerun it after changing the layout.

    python scripts/render_layers.py [--theme Dark|Light] [--scale 1.6]

Needs: pip install PyQt5 simpleeval (vial-gui is auto-cloned into .cache/).
"""
import argparse
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VIAL_GUI_TAG = "v0.7.5"


def vial_gui_src(path):
    path = path or os.path.join(ROOT, ".cache", "vial-gui")
    if not os.path.isdir(os.path.join(path, "src")):
        subprocess.check_call(["git", "clone", "-q", "--depth", "1", "--branch", VIAL_GUI_TAG,
                               "https://github.com/vial-kb/vial-gui.git", path])
    return os.path.join(path, "src", "main", "python")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--vil", default=os.path.join(ROOT, "layout", "cornelious.vil"))
    ap.add_argument("--definition", default=os.path.join(ROOT, "qmk", "keyboards", "cornelious", "keymaps", "vial", "vial.json"))
    ap.add_argument("--out", default=os.path.join(ROOT, "docs", "layers"))
    ap.add_argument("--theme", default="Dark")
    ap.add_argument("--scale", type=float, default=1.6)
    ap.add_argument("--vial-gui")
    args = ap.parse_args()

    src = vial_gui_src(args.vial_gui)
    sys.path.insert(0, src)
    if sys.platform != "win32":  # off-screen Qt has no fonts on Windows; there the widget just stays hidden
        os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from PyQt5.QtCore import QPoint
    from PyQt5.QtGui import QFont, QPainter, QPixmap, QPalette
    from PyQt5.QtWidgets import QApplication

    app = QApplication([])
    font = QFont("Segoe UI" if sys.platform == "win32" else "DejaVu Sans")
    font.setPointSize(9)
    app.setFont(font)

    from themes import Theme
    from keycodes.keycodes import recreate_keyboard_keycodes
    from kle_serial import Serial as KleSerial
    from util import KeycodeDisplay
    from widgets.keyboard_widget import KeyboardWidget

    Theme.set_theme(args.theme)

    vil = json.load(open(args.vil, encoding="utf-8"))
    definition = json.load(open(args.definition, encoding="utf-8"))

    class Board:
        """The parts of a vial-gui Keyboard that labels and the widget need."""
        vial_protocol = vil.get("vial_protocol", 6)
        layers = len(vil["layout"])
        macro_count = len(vil.get("macro", []))
        tap_dance_count = len(vil.get("tap_dance", []))
        custom_keycodes = definition.get("customKeycodes")
        midi = None
        supported_features = set()

    recreate_keyboard_keycodes(Board)

    keys = []
    for key in KleSerial().deserialize(definition["layouts"]["keymap"]).keys:
        key.row, key.col = map(int, key.labels[0].split(","))
        key.layout_index, key.layout_option = -1, -1
        if key.labels[8]:
            key.layout_index, key.layout_option = map(int, key.labels[8].split(","))
        keys.append(key)

    class LayoutEditor:
        def get_choice(self, idx):
            return 0

    widget = KeyboardWidget(LayoutEditor())
    widget.set_keys(keys, [])
    widget.scale = args.scale

    os.makedirs(args.out, exist_ok=True)
    bg = QApplication.palette().color(QPalette.Window)
    written = []
    for layer, rows in enumerate(vil["layout"]):
        codes = [rows[w.desc.row][w.desc.col] for w in widget.widgets]
        if layer > 0 and all(c in ("KC_TRNS", 1) for c in codes):
            continue
        widget.update_layout()
        for w, code in zip(widget.widgets, codes):
            KeycodeDisplay.display_keycode(w, code)
        size = widget.minimumSizeHint()  # (KeyboardWidget shadows width()/height())
        widget.resize(size)
        pad = 16
        pm = QPixmap(size.width() + 2 * pad, size.height() + 2 * pad)
        pm.fill(bg)
        qp = QPainter(pm)
        widget.render(qp, QPoint(pad, pad))
        qp.end()
        path = os.path.join(args.out, "layer-{}.png".format(layer))
        pm.save(path)
        written.append(path)
    for p in written:
        print("wrote", os.path.relpath(p, ROOT))


if __name__ == "__main__":
    main()
