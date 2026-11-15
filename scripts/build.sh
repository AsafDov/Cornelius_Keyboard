#!/usr/bin/env bash
# Build Cornelious firmware with vial-qmk (Linux, WSL or GitHub Actions).
#
#   scripts/build.sh              build every board in qmk/keyboards/cornelious/
#   scripts/build.sh rp2040zero   build one board
#
# First run sets everything up under $CORNELIOUS_WORK (default ~/.cache/cornelious),
# no root needed: a Python venv with the QMK CLI, the QMK ARM toolchain, vial-qmk
# at a pinned commit, and vial-gui (for decoding the .vil). Later runs reuse it.
#
# Each build regenerates keymap.c from layout/cornelious.vil, so the .vil is the
# only file you ever edit for layout changes. Output goes to firmware/.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WORK="${CORNELIOUS_WORK:-$HOME/.cache/cornelious}"

# Pinned versions. Bump deliberately, then rebuild and test on a board.
VIAL_QMK_REPO="https://github.com/vial-kb/vial-qmk.git"
VIAL_QMK_REF="dd43959ae5c08d8a28d38a1acf7b04e86b14a344"   # vial branch, 2026-07-26
VIAL_GUI_REPO="https://github.com/vial-kb/vial-gui.git"
VIAL_GUI_TAG="v0.7.5"
TOOLCHAIN_URL="https://github.com/qmk/qmk_toolchains/releases/download/v15.2.0-1/qmk_toolchains-gcc15.2.0-host_linuxX64.tar.zst"

log() { printf '\n== %s\n' "$*"; }

mkdir -p "$WORK"
cd "$WORK"

# --- Python venv: QMK CLI + what the generator needs
if [ ! -x venv/bin/python ]; then
    log "creating Python venv"
    python3 -m venv venv
fi
if ! venv/bin/python -c "import qmk, simpleeval, zstandard" 2>/dev/null; then
    log "installing Python packages"
    venv/bin/pip install -q --upgrade pip
    venv/bin/pip install -q qmk simpleeval zstandard
fi

# --- ARM toolchain
if [ ! -x toolchain/qmk_toolchains_linuxX64/bin/arm-none-eabi-gcc ]; then
    log "downloading QMK toolchain"
    rm -rf toolchain && mkdir -p toolchain
    curl -fsSL -o tc.tar.zst "$TOOLCHAIN_URL"
    venv/bin/python -c "import sys, zstandard; zstandard.ZstdDecompressor().copy_stream(open('tc.tar.zst','rb'), sys.stdout.buffer)" \
        | tar -x -C toolchain
    rm -f tc.tar.zst
fi
export PATH="$WORK/venv/bin:$WORK/toolchain/qmk_toolchains_linuxX64/bin:$PATH"

# --- vial-qmk
if [ ! -d vial-qmk/.git ]; then
    log "cloning vial-qmk"
    git clone -q --filter=blob:none -b vial "$VIAL_QMK_REPO" vial-qmk
fi
if [ "$(git -C vial-qmk rev-parse HEAD)" != "$VIAL_QMK_REF" ]; then
    log "checking out vial-qmk $VIAL_QMK_REF"
    git -C vial-qmk fetch -q origin vial
    git -C vial-qmk checkout -q "$VIAL_QMK_REF"
    git -C vial-qmk submodule update -q --init --recursive --depth 1
    venv/bin/pip install -q -r vial-qmk/requirements.txt
fi
export QMK_HOME="$WORK/vial-qmk"

# --- vial-gui (keycode tables for reading the .vil)
if [ ! -d vial-gui/.git ]; then
    log "cloning vial-gui $VIAL_GUI_TAG"
    git clone -q --depth 1 --branch "$VIAL_GUI_TAG" "$VIAL_GUI_REPO" vial-gui
fi

# --- generate keymap.c from the .vil
log "generating keymap from layout/cornelious.vil"
python "$ROOT/scripts/vil2keymap.py" --qmk "$WORK/vial-qmk" --vial-gui "$WORK/vial-gui"

# --- copy our keyboard into the vial-qmk tree
rm -rf vial-qmk/keyboards/cornelious
cp -r "$ROOT/qmk/keyboards/cornelious" vial-qmk/keyboards/cornelious

# --- build
boards=("$@")
if [ ${#boards[@]} -eq 0 ]; then
    for kj in "$ROOT"/qmk/keyboards/cornelious/*/keyboard.json; do
        boards+=("$(basename "$(dirname "$kj")")")
    done
fi

mkdir -p "$ROOT/firmware"
cd vial-qmk
for b in "${boards[@]}"; do
    log "building cornelious/$b:vial"
    make -j"$(nproc)" "cornelious/$b:vial"
    for f in cornelious_"${b}"_vial.*; do
        case "$f" in *.uf2|*.hex|*.bin) cp "$f" "$ROOT/firmware/$f"; echo "-> firmware/$f" ;; esac
    done
done
