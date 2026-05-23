"""Phase 5 — rendered carousels → Drive + Publer.

Uploads each slide PNG to the configured Drive folder, schedules a carousel on
Publer per target platform, and appends to runs/<run_id>/published.json so
re-running the same source can skip already-published items.
"""
from __future__ import annotations

from pathlib import Path

from ..config import Config


def run(config: Config, slides_dir: Path, run_dir: Path) -> Path:
    """Publish one rendered carousel. Returns the path to the published.json record."""
    raise NotImplementedError("Phase 5 not yet implemented")
