"""Onboarding gate tests — config validation, no LLM calls."""
from __future__ import annotations

from pathlib import Path

import pytest

from live_to_carousel import config as cfg
from live_to_carousel.onboarding import assert_ready


def _make_config(tmp_path: Path, **overrides) -> cfg.Config:
    png = tmp_path / "template.png"
    png.write_bytes(b"\x89PNG\r\n\x1a\n")
    slot = tmp_path / "slots.json"
    slot.write_text("{}")
    voice = tmp_path / "voice.md"
    voice.write_text("sample")
    base = cfg.Config(
        source=cfg.SourceConfig(type="youtube"),
        template=cfg.TemplateConfig(png_path=str(png), slot_map_path=str(slot)),
        brand=cfg.BrandConfig(primary_hex="#000000"),
        voice=cfg.VoiceConfig(samples_path=str(voice)),
        output=cfg.OutputConfig(platforms=["linkedin"]),
    )
    return base.model_copy(update=overrides)


def test_ready_config_has_no_problems(tmp_path: Path) -> None:
    assert assert_ready(_make_config(tmp_path)) == []


def test_missing_template_png_reports_problem(tmp_path: Path) -> None:
    c = _make_config(tmp_path, template=cfg.TemplateConfig(
        png_path=str(tmp_path / "nope.png"),
        slot_map_path=str(tmp_path / "slots.json"),
    ))
    problems = assert_ready(c)
    assert any("template.png_path missing" in p for p in problems)


def test_missing_voice_samples_reports_problem(tmp_path: Path) -> None:
    c = _make_config(tmp_path, voice=cfg.VoiceConfig())
    problems = assert_ready(c)
    assert any("voice needs samples_path" in p for p in problems)


def test_empty_platforms_reports_problem(tmp_path: Path) -> None:
    c = _make_config(tmp_path, output=cfg.OutputConfig(platforms=[]))
    problems = assert_ready(c)
    assert any("output.platforms is empty" in p for p in problems)


def test_save_then_load_roundtrip(tmp_path: Path) -> None:
    c = _make_config(tmp_path)
    out = tmp_path / "config.json"
    cfg.save(c, out)
    loaded = cfg.load(out)
    assert loaded.template.png_path == c.template.png_path
    assert loaded.output.platforms == ["linkedin"]


def test_load_missing_file_raises(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        cfg.load(tmp_path / "does_not_exist.json")
