"""Config schema + load/save. Phase 0 writes this; every later phase reads it."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field

CONFIG_PATH = Path("config.json")


class SourceConfig(BaseModel):
    """Default source type for runs. Each run can override via CLI."""

    type: Literal["youtube", "audio", "doc", "thread"]
    default_url_or_path: str | None = None


class TemplateConfig(BaseModel):
    """Carousel template — PNG + slot map describing where text/image goes."""

    png_path: str
    slot_map_path: str
    aspect_ratio: Literal["1:1", "4:5", "9:16"] = "4:5"


class BrandConfig(BaseModel):
    primary_hex: str
    accent_hex: str | None = None
    font_paths: list[str] = Field(default_factory=list)
    logo_path: str | None = None


class VoiceConfig(BaseModel):
    """Either samples_path (markdown file of past posts) or inline samples."""

    samples_path: str | None = None
    inline_samples: list[str] = Field(default_factory=list)
    language: Literal["ar", "en", "mixed"] = "ar"
    dialect: str | None = None
    banned_chars: list[str] = Field(default_factory=list)
    no_trailing_periods: bool = True


class OutputConfig(BaseModel):
    drive_folder_id: str | None = None
    publer_workspace_id: str | None = None
    platforms: list[Literal["instagram", "linkedin", "x", "tiktok"]] = Field(default_factory=list)


class CadenceConfig(BaseModel):
    slides_per_carousel: int = 5
    carousels_per_source: int = 3


class SecretsConfig(BaseModel):
    """Paths to credential files. Never store secrets inline."""

    anthropic_api_key_env: str = "ANTHROPIC_API_KEY"
    publer_api_key_env: str = "PUBLER_API_KEY"
    google_service_account_path: str | None = None


class Config(BaseModel):
    version: int = 1
    source: SourceConfig
    template: TemplateConfig
    brand: BrandConfig
    voice: VoiceConfig
    output: OutputConfig
    cadence: CadenceConfig = Field(default_factory=CadenceConfig)
    secrets: SecretsConfig = Field(default_factory=SecretsConfig)


def load(path: Path = CONFIG_PATH) -> Config:
    if not path.exists():
        raise FileNotFoundError(
            f"{path} not found. Run `ltc init` to create it."
        )
    data = json.loads(path.read_text(encoding="utf-8"))
    return Config.model_validate(data)


def save(config: Config, path: Path = CONFIG_PATH) -> None:
    path.write_text(
        json.dumps(config.model_dump(mode="json"), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def exists(path: Path = CONFIG_PATH) -> bool:
    return path.exists()
