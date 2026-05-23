"""Phase 1 — source → transcript.md.

YouTube live / podcast audio go through Whisper (large-v3-turbo by default).
Docs and threads pass through unchanged. Writes runs/<run_id>/transcript.md.
"""
from __future__ import annotations

from pathlib import Path

from ..config import Config


def run(config: Config, source: str, run_dir: Path) -> Path:
    """Produce a transcript.md from the given source. Returns the path written."""
    raise NotImplementedError("Phase 1 not yet implemented")
