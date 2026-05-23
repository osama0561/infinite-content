"""Phase 2 — transcript → ranked idea candidates.

Claude pass extracts claims, contrarian takes, stories, named numbers. Each
candidate is scored on hook strength, novelty, proof level, self-containment,
then de-duplicated against history/ideas.jsonl. Writes runs/<run_id>/ideas.json.
"""
from __future__ import annotations

from pathlib import Path

from ..config import Config


def run(config: Config, transcript_path: Path, run_dir: Path) -> Path:
    """Produce ideas.json from a transcript. Returns the path written."""
    raise NotImplementedError("Phase 2 not yet implemented")
