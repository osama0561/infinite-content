"""Phase 3 — top ideas → slide scripts.

For each selected idea, generate slide-by-slide text using voice samples as
few-shot. Enforces voice rules from config (banned chars, no trailing periods,
dialect lock). Locks any numbers to their source quote to prevent LLM drift.
Writes runs/<run_id>/carousel_<n>.json.
"""
from __future__ import annotations

from pathlib import Path

from ..config import Config


def run(config: Config, ideas_path: Path, run_dir: Path) -> list[Path]:
    """Produce one carousel_<n>.json per selected idea. Returns the paths written."""
    raise NotImplementedError("Phase 3 not yet implemented")
