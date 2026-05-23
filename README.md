# live-to-carousel

Turn long-form source material — YouTube live transcripts, podcast audio, docs, threads — into platform-ready carousel posts. Five stages, one onboarding gate, idea de-dup across runs.

## Status

Early scaffold. Phase 0 (onboarding) lands first; pipeline stages follow.

## Pipeline

```
source  ─►  extract  ─►  ideas  ─►  script  ─►  render  ─►  publish
                  transcript   ranked    slide       PNG        Drive +
                               claims    text                   Publer
```

Onboarding (Phase 0) gates everything. If `config.json` is missing required fields, the CLI refuses to run.

## Quick start

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e .
ltc init      # Phase 0 onboarding wizard
ltc run <source>
```

## What you need before first run

- Source: YouTube URL, audio file, or text file
- Carousel template: PNG + slot map JSON (or one of your previous carousels to extract slots from)
- Voice samples: 5–10 of your best past posts, or a path to a voice spec markdown file
- Brand: primary hex, font file(s), logo PNG
- Output: Drive folder ID, Publer workspace, target platforms
- API keys: Anthropic, optionally Publer + Google Drive service account

## Why this exists

Most "content from transcript" tools paraphrase generically. This one:

- Refuses to run without a real template and voice samples — no generic output
- Logs every published idea so reruns don't repeat the same claim
- Locks numbers to source quotes — no LLM drift on stats
- Enforces voice rules per run (e.g. no trailing periods, banned punctuation, dialect lock)
