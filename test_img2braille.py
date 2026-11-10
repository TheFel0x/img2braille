"""Tests for img2braille."""

import os
import subprocess
import sys
from pathlib import Path

from PIL import Image

REPO_ROOT = Path(__file__).resolve().parent


def run_img2braille(*argv):
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    return subprocess.run(
        [sys.executable, "img2braille.py", *argv],
        capture_output=True,
        encoding="utf-8",
        cwd=REPO_ROOT,
        env=env,
    )


def test_missing_input_file_reports_clean_error():
    """A missing image must exit non-zero with a message, not a traceback."""
    proc = run_img2braille("does-not-exist.png")
    assert proc.returncode != 0
    assert "does-not-exist.png" in proc.stderr
    assert "Traceback" not in proc.stderr


def test_small_image_converts(tmp_path):
    """A tiny image still converts and prints braille output."""
    image_path = tmp_path / "tiny.png"
    Image.new("RGB", (8, 8), "white").save(image_path)
    proc = run_img2braille(str(image_path), "-w", "4")
    assert proc.returncode == 0, proc.stderr
    assert any(ord(char) in range(0x2800, 0x2900) for char in proc.stdout)

