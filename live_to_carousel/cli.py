"""`ltc` entry point.

    ltc init         — run Phase 0 onboarding wizard
    ltc check        — validate config.json without running anything
    ltc run <src>    — execute the pipeline (refuses if onboarding incomplete)
"""
from __future__ import annotations

import sys

import click

from . import config as cfg
from . import onboarding


@click.group()
def main() -> None:
    """live-to-carousel — long-form source → ranked ideas → carousel PNGs → published."""


@main.command("init")
def init_cmd() -> None:
    """Run the onboarding wizard. Overwrites config.json."""
    if cfg.exists():
        if not click.confirm("config.json exists. Overwrite?", default=False):
            click.echo("aborted")
            return
    onboarding.run_wizard()


@main.command("check")
def check_cmd() -> None:
    """Validate config.json. Exits non-zero if anything is missing."""
    try:
        config = cfg.load()
    except FileNotFoundError as e:
        click.echo(str(e), err=True)
        sys.exit(2)
    problems = onboarding.assert_ready(config)
    if problems:
        click.echo("config.json is incomplete:", err=True)
        for p in problems:
            click.echo(f"  - {p}", err=True)
        sys.exit(1)
    click.echo("config.json OK — pipeline ready")


@main.command("run")
@click.argument("source", required=False)
def run_cmd(source: str | None) -> None:
    """Execute the full pipeline against SOURCE (URL or path)."""
    try:
        config = cfg.load()
    except FileNotFoundError as e:
        click.echo(str(e), err=True)
        sys.exit(2)
    problems = onboarding.assert_ready(config)
    if problems:
        click.echo("Pipeline gate closed. Fix these and re-run `ltc check`:", err=True)
        for p in problems:
            click.echo(f"  - {p}", err=True)
        sys.exit(1)
    source = source or config.source.default_url_or_path
    if not source:
        click.echo("no SOURCE argument and no default in config.source.default_url_or_path", err=True)
        sys.exit(2)
    click.echo(f"[ok] gate open — would run pipeline on: {source}")
    click.echo("(pipeline stages 1–5 not yet implemented)")


if __name__ == "__main__":
    main()
