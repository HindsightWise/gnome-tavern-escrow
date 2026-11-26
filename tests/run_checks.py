"""Deterministic test & negative-control harness for Gnome Tavern Gno.land realm."""
from __future__ import annotations

import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REALM_DIR = PROJECT_ROOT / "gno" / "r" / "nym-tavern247" / "tavern"
DEFAULT_GNO_BIN = shutil.which("gno") or "/Users/zerbytheboss/go/bin/gno"
GNO_BIN = Path(os.getenv("GNO_BIN", DEFAULT_GNO_BIN))
GNO_ROOT = os.getenv("GNO_ROOT", "/Users/zerbytheboss/.gemini/antigravity/scratch/repos/gnolang-gno")


def run_gno_test(cwd: Path) -> subprocess.CompletedProcess[str]:
    cmd = [str(GNO_BIN), "test", "-v"]
    if GNO_ROOT and Path(GNO_ROOT).is_dir():
        cmd.extend(["-root-dir", GNO_ROOT])
    cmd.append(".")
    return subprocess.run(
        cmd,
        cwd=str(cwd),
        capture_output=True,
        text=True,
        check=False,
    )


def main() -> int:
    if not GNO_BIN.is_file():
        print(f"ERROR: gno binary not found at {GNO_BIN}", file=sys.stderr)
        return 2

    if os.getenv("CORRUPT_GATE_CONTROL", "").strip() == "1":
        with tempfile.TemporaryDirectory(prefix="tavern-corrupt-") as tmp:
            dst = Path(tmp) / "tavern"
            shutil.copytree(REALM_DIR, dst)
            src_file = dst / "tavern.gno"
            text = src_file.read_text(encoding="utf-8")
            corrupted = text.replace("totalLocked -= payout", "totalLocked -= 0", 1)
            assert corrupted != text, "Failed to inject escrow corruption mutant"
            src_file.write_text(corrupted, encoding="utf-8")
            proc = run_gno_test(dst)
            print("[NEGATIVE_CONTROL] Injected escrow conservation fault; gno test exit =", proc.returncode)
            if proc.returncode == 0:
                print("ERROR: Negative control mutant unexpectedly passed!", file=sys.stderr)
                return 0
            print(proc.stdout)
            return 1

    proc = run_gno_test(REALM_DIR)
    print(proc.stdout, end="")
    if proc.stderr:
        print(proc.stderr, end="", file=sys.stderr)
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
