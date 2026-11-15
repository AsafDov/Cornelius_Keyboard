#!/usr/bin/env python3
"""Talk to a Vial keyboard over USB without opening the Vial app.

save/load run vial-gui's own code headlessly, so the result is exactly what
Vial's File > Save current layout / Load saved layout would do.

    python scripts/vial_tool.py list
    python scripts/vial_tool.py save out.vil  [--device VID:PID]
    python scripts/vial_tool.py load in.vil   [--device VID:PID]
    python scripts/vial_tool.py bootloader    [--device VID:PID]

`bootloader` reboots the board into its UF2 bootloader (needs only hidapi, and a
board built in insecure mode, like ours), so you can flash without touching it.

Needs: pip install PyQt5 hidapi simpleeval, plus a vial-gui checkout
(auto-cloned into .cache/vial-gui). Prefer the Vial app for day-to-day use;
this is for scripting and for checking that two boards hold the same layout.
"""
import argparse
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
    ap.add_argument("action", choices=["list", "save", "load", "bootloader"])
    ap.add_argument("file", nargs="?")
    ap.add_argument("--device", help="VID:PID in hex, e.g. FEED:C0E1 (needed when several Vial boards are plugged in)")
    ap.add_argument("--vial-gui", help="vial-gui checkout")
    args = ap.parse_args()

    if args.action == "bootloader":
        return bootloader(args.device)

    src = vial_gui_src(args.vial_gui)
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    sys.path.insert(0, src)
    from PyQt5.QtWidgets import QApplication

    app = QApplication([])  # noqa: F841
    from editor.qmk_settings import QmkSettings
    from hidproxy import hid
    from vial_device import VialKeyboard

    class Ctx:
        def get_resource(self, name):
            return os.path.join(src, "..", "resources", "base", name)

    QmkSettings.initialize(Ctx())

    devs = [d for d in hid.enumerate()
            if d["usage_page"] == 0xFF60 and d["usage"] == 0x61 and "vial:f64c2b3c" in (d["serial_number"] or "").lower()]
    if args.action == "list":
        for d in devs:
            print("{:04X}:{:04X}  {} {}".format(d["vendor_id"], d["product_id"], d["manufacturer_string"], d["product_string"]))
        return
    if args.device:
        vid, pid = (int(x, 16) for x in args.device.split(":"))
        devs = [d for d in devs if d["vendor_id"] == vid and d["product_id"] == pid]
    if len(devs) != 1:
        sys.exit("found {} Vial boards; use --device VID:PID (see `list`)".format(len(devs)))
    if not args.file:
        ap.error("file is required")

    kb = VialKeyboard(devs[0])
    kb.open()
    k = kb.keyboard
    if args.action == "save":
        open(args.file, "wb").write(k.save_layout())
        print("saved", args.file)
    else:
        k.restore_layout(open(args.file, "rb").read())
        print("loaded", args.file)
    k.dev.close()


def bootloader(device):
    """VIA command 0x0B (bootloader jump). Vial only obeys it while unlocked."""
    import hid

    devs = [d for d in hid.enumerate()
            if d["usage_page"] == 0xFF60 and d["usage"] == 0x61 and "vial:f64c2b3c" in (d["serial_number"] or "").lower()]
    if device:
        vid, pid = (int(x, 16) for x in device.split(":"))
        devs = [d for d in devs if d["vendor_id"] == vid and d["product_id"] == pid]
    if len(devs) != 1:
        sys.exit("found {} Vial boards; use --device VID:PID (see `list`)".format(len(devs)))
    h = hid.device()
    h.open_path(devs[0]["path"])
    h.write(b"\x00\x0b" + b"\x00" * 31)
    h.close()
    print("sent bootloader jump; an RPI-RP2 drive should appear in a few seconds")


if __name__ == "__main__":
    main()
