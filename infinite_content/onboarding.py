"""Phase 0 — interactive onboarding wizard. Writes config.json.

The pipeline refuses to run until every required field here resolves to a real
value pointing at a real file (where applicable). No silent best-guess.
"""
from __future__ import annotations

from pathlib import Path

import click

from .config import (
    BrandConfig,
    CadenceConfig,
    Config,
    OutputConfig,
    SecretsConfig,
    SourceConfig,
    TemplateConfig,
    VoiceConfig,
    save,
)


def _prompt_path(label: str, must_exist: bool = True, optional: bool = False) -> str | None:
    while True:
        raw = click.prompt(label, default="", show_default=False).strip()
        if not raw:
            if optional:
                return None
            click.echo("  required — try again")
            continue
        p = Path(raw).expanduser()
        if must_exist and not p.exists():
            click.echo(f"  not found: {p}")
            continue
        return str(p)


def run_wizard() -> Config:
    click.echo("infinite-content — onboarding")
    click.echo("This is a one-time setup. Every field is required unless marked optional.\n")

    click.echo("# Source")
    src_type = click.prompt(
        "  default source type",
        type=click.Choice(["youtube", "audio", "doc", "thread"]),
        default="youtube",
    )
    source = SourceConfig(type=src_type)

    click.echo("\n# Carousel template")
    click.echo("  Drop a PNG of your template and a JSON slot map describing where text/image goes.")
    template = TemplateConfig(
        png_path=_prompt_path("  template PNG path"),
        slot_map_path=_prompt_path("  slot map JSON path"),
        aspect_ratio=click.prompt(
            "  aspect ratio", type=click.Choice(["1:1", "4:5", "9:16"]), default="4:5"
        ),
    )

    click.echo("\n# Brand")
    brand = BrandConfig(
        primary_hex=click.prompt("  primary hex (e.g. #1a1a1a)"),
        accent_hex=click.prompt("  accent hex (optional)", default="", show_default=False) or None,
        font_paths=[
            p for p in (
                _prompt_path("  font file path (or blank to skip)", optional=True),
            ) if p
        ],
        logo_path=_prompt_path("  logo PNG path (optional)", optional=True),
    )

    click.echo("\n# Voice")
    click.echo("  Point at a markdown file of past posts, or skip to add inline later.")
    voice = VoiceConfig(
        samples_path=_prompt_path("  voice samples path (e.g. youtube/voice.md)", optional=True),
        language=click.prompt(
            "  language", type=click.Choice(["ar", "en", "mixed"]), default="ar"
        ),
        dialect=click.prompt("  dialect (optional, e.g. Najdi)", default="", show_default=False) or None,
    )

    click.echo("\n# Output targets")
    output = OutputConfig(
        drive_folder_id=click.prompt("  Drive folder ID (optional)", default="", show_default=False) or None,
        publer_workspace_id=click.prompt("  Publer workspace ID (optional)", default="", show_default=False) or None,
        platforms=[
            p.strip() for p in click.prompt(
                "  platforms (comma-separated: instagram,linkedin,x,tiktok)",
                default="linkedin",
            ).split(",") if p.strip()
        ],
    )

    click.echo("\n# Cadence")
    cadence = CadenceConfig(
        slides_per_carousel=click.prompt("  slides per carousel", type=int, default=5),
        carousels_per_source=click.prompt("  carousels per source", type=int, default=3),
    )

    click.echo("\n# Secrets")
    click.echo("  API keys are read from env vars at runtime — only env var NAMES are stored.")
    secrets = SecretsConfig(
        anthropic_api_key_env=click.prompt(
            "  Anthropic API key env var name", default="ANTHROPIC_API_KEY"
        ),
        publer_api_key_env=click.prompt(
            "  Publer API key env var name", default="PUBLER_API_KEY"
        ),
        google_service_account_path=_prompt_path(
            "  Google service account JSON path (optional)", optional=True
        ),
    )

    config = Config(
        source=source,
        template=template,
        brand=brand,
        voice=voice,
        output=output,
        cadence=cadence,
        secrets=secrets,
    )
    save(config)
    click.echo("\nWrote config.json. Pipeline gate now open.")
    return config


def assert_ready(config) -> list[str]:
    """Return list of problems. Empty list = ready to run."""
    problems: list[str] = []
    if not Path(config.template.png_path).exists():
        problems.append(f"template.png_path missing: {config.template.png_path}")
    if not Path(config.template.slot_map_path).exists():
        problems.append(f"template.slot_map_path missing: {config.template.slot_map_path}")
    if config.voice.samples_path and not Path(config.voice.samples_path).exists():
        problems.append(f"voice.samples_path missing: {config.voice.samples_path}")
    if not config.voice.samples_path and not config.voice.inline_samples:
        problems.append("voice needs samples_path OR inline_samples; both empty")
    if not config.output.platforms:
        problems.append("output.platforms is empty — set at least one")
    return problems
