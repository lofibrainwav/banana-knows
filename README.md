# VibeCoding Knowledge Management System

[![CI Status](https://github.com/your_org/your_repo/actions/workflows/ci.yml/badge.svg)]
[![Coverage](coverage.svg)]

A pipeline to automate YouTube transcript extraction, multi-stage LLM analysis, and Obsidian vault integration.

## Features

- YouTube transcript ingestion with proxy support
- Fallback transcription via CTranslate2/WhisperX
- HTML/Markdown rendering for analysis results (Obsidian compatible)
- Batch renderer to process JSON outputs into vault notes
- Meta-data frontmatter (title, date, tags, source)
- Internal link normalization for Obsidian wiki-links

## Installation

```bash
git clone https://github.com/your_org/your_repo.git
cd your_repo
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Usage

### HTML/Markdown Renderer

```bash
# Render a single file:
python3 scripts/html_renderer.py md '{"title":"My Note","content":"Hello [[World]]","date":"2024-01-01","tags":["test"],"source":"api"}' output.md
python3 scripts/html_renderer.py html '{"title":"My Note","content":"Hello [[World]]"}' output.html
```

### Batch Renderer

```bash
# Process all JSON files in input_dir into vault_dir
python3 scripts/batch_renderer.py input_dir vault_dir
```

## Testing

Run the full test suite with coverage:

```bash
source venv/bin/activate
coverage run -m pytest --disable-warnings -q
coverage report -m
```

## CI Integration

GitHub Actions workflow defined in `.github/workflows/ci.yml` runs lint, tests, and coverage on each push/PR to `main`.

## License

This project is licensed under the MIT License. 