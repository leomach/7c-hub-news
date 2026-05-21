# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**7C Hub News** is a three-stage pipeline that collects tech news from multiple sources, curates it with AI (Gemini), and delivers a daily bulletin via Telegram. It runs automatically on weekdays at 07:00 BRT via GitHub Actions.

```
sources.yaml
    ↓
[Collector (Go)]  → output/news.json
    ↓
[Processor (Python)] → output/bulletin.txt
    ↓
[Deliverer (Python)] → Telegram API
```

## Running the Pipeline

### Stage 1 — Collector (Go)
```bash
cd collector
go run main.go -config ../sources.yaml -output ../output/news.json
```

### Stage 2 — Processor (Python)
```bash
pip install -r processor/requirements.txt
# Requires LLM_API_KEY, LLM_BASE_URL, LLM_MODEL in processor/.env
python3 -m processor.main
```

### Stage 3 — Deliverer (Python)
```bash
pip install -r deliverer/requirements.txt
# Requires TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID in deliverer/.env
python3 -m deliverer.main --input output/bulletin.txt
```

### Collector — Build & Test
```bash
cd collector
go build ./...
go test ./...
go vet ./...
```

## Architecture

### Collector (Go)

Concurrent fetcher orchestrated by `collector/main.go`. Each source in `sources.yaml` gets a goroutine. Three concrete `Fetcher` implementations:

- `fetcher/rss.go` — Generic RSS/Atom via `gofeed`
- `fetcher/hackernews.go` — HN Firebase REST API (fetches items concurrently)
- `fetcher/tabnews.go` — TabNews REST API

After fetching, items are filtered by `max_age_hours` and deduplicated by normalized URL (`dedup/dedup.go`). Output is written to `news.json` via `output/writer.go`.

### Processor (Python)

Reads `news.json`, applies quota-based selection (top-N by `original_score` per category: global/national/regional), then for each selected item:

1. **Translator** (`llm/translator.py`) — Calls Gemini to translate non-PT content to PT-BR
2. **Summarizer** (`llm/summarizer.py`) — Generates ≤2-sentence, ≤280-char summary
3. **Formatter** (`pipeline/formatter.py`) — Builds HTML bulletin with emojis for Telegram

Prompts live in `processor/prompts/` (`translate.txt`, `summarize.txt`).
Settings are loaded from both `sources.yaml` and environment variables via `processor/config/settings.py` (pydantic-settings).

### Deliverer (Python)

`deliverer/telegram.py` sends the bulletin to Telegram via HTTP API. Splits messages at 4096 chars (Telegram limit). Retries up to 3 times with exponential backoff using `tenacity`.

## Central Configuration

**`sources.yaml`** controls everything:
- `settings` — `max_age_hours`, `fetch_timeout_seconds`, `max_concurrent_fetches`
- `quotas` — per-category item limits (`global`, `national`, `regional`)
- `sources` — list of news sources (each has `type`: `rss`, `hackernews`, or `tabnews`)
- `llm` — provider, model, `base_url`, `max_tokens`, `temperature`

## Environment Variables

| Variable | Used by | Purpose |
|---|---|---|
| `LLM_API_KEY` | Processor | Gemini API key |
| `LLM_BASE_URL` | Processor | Gemini API base URL |
| `LLM_MODEL` | Processor | Model name (e.g. `gemini-1.5-flash`) |
| `TELEGRAM_BOT_TOKEN` | Deliverer | Bot token |
| `TELEGRAM_CHAT_ID` | Deliverer | Target chat/channel ID |

In CI these are GitHub Actions secrets. Locally, place them in `.env` files inside each component's directory.

## Key Data Models

**`NewsItem`** (defined in Go `collector/model/model.go` and mirrored in Python `processor/models/news_item.py`):
- `title`, `url`, `source_name`, `source_category`, `published_at`
- `original_score` — raw relevance score from the source (used for quota selection)
- `translated_title`, `translated_content`, `summary` — added by processor

**`news.json`** structure: `{ metadata, items: [NewsItem], errors: [CollectorError] }`

**`bulletin.txt`** structure: metadata header block + `---` separator + HTML-formatted body

## CI/CD

`.github/workflows/daily_news.yml` runs three sequential jobs: `collect` → `process` → `deliver`. A `notify_failure` job sends a Telegram alert on any failure. Manual trigger is available via `workflow_dispatch`.
