#!/usr/bin/env python3
"""
scripts/batch_renderer.py

Walk an input directory of JSON files and render each into Markdown and HTML files
for an Obsidian vault.
"""
import os
import sys
import json
import logging
from scripts.html_renderer import render_markdown, render_html

# Configure basic logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def process_file(json_path: str, vault_dir: str) -> (bool, bool):
    """
    Load JSON data and render markdown and HTML into vault_dir.
    """
    md_ok = False
    html_ok = False
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        logging.error(f"Invalid JSON in {json_path}: {e}")
        return md_ok, html_ok
    # Prepare output filenames
    base = os.path.splitext(os.path.basename(json_path))[0]
    md_path = os.path.join(vault_dir, f"{base}.md")
    html_path = os.path.join(vault_dir, f"{base}.html")
    try:
        render_markdown(data, md_path)
        logging.info(f"Generated Markdown: {md_path}")
        md_ok = True
    except Exception as e:
        logging.error(f"Failed to render markdown for {json_path}: {e}")
    try:
        render_html(data, html_path)
        logging.info(f"Generated HTML: {html_path}")
        html_ok = True
    except Exception as e:
        logging.error(f"Failed to render HTML for {json_path}: {e}")
    return md_ok, html_ok


def main(args=None):
    """
    CLI entry point: batch_renderer.py <input_dir> <vault_dir>
    """
    if args is None:
        args = sys.argv[1:]
    if len(args) < 2:
        print("Usage: batch_renderer.py <input_dir> <vault_dir>")
        sys.exit(1)
    input_dir, vault_dir = args[0], args[1]
    if not os.path.isdir(input_dir):
        logging.error(f"Input directory not found: {input_dir}")
        sys.exit(1)
    os.makedirs(vault_dir, exist_ok=True)
    # Walk directory and collect metrics
    total = 0
    md_success = 0
    html_success = 0
    for root, _, files in os.walk(input_dir):
        for fname in files:
            if fname.lower().endswith('.json'):
                total += 1
                json_path = os.path.join(root, fname)
                md_ok, html_ok = process_file(json_path, vault_dir)
                if md_ok:
                    md_success += 1
                if html_ok:
                    html_success += 1
    # Summary
    logging.info(f"Batch rendering complete: {total} files, {md_success} markdown success, {html_success} HTML success.")


if __name__ == '__main__':
    main() 