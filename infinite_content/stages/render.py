"""Phase 4 — slide scripts → PNGs.

PIL with raqm for Arabic. Reads template PNG + slot map from config; pastes
text/image into each slot per slide. Emits one slide_NN.png per slide and
optionally re-renders per platform aspect ratio.
Writes runs/<run_id>/carousel_<n>/slide_*.png.
"""
from __future__ import annotations

from pathlib import Path

from ..config import Config


def run(config: Config, script_path: Path, run_dir: Path) -> list[Path]:
    """Render slides for one carousel script. Returns the PNG paths written."""
    raise NotImplementedError("Phase 4 not yet implemented")
