#!/usr/bin/env python3
"""
scripts/html_renderer.py

Render analysis data into Markdown and HTML for Obsidian integration.
"""

import os
import sys
import json
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
import re

# Convert Obsidian wiki-links [[Page]] to markdown links
def normalize_links(content: str) -> str:
    return re.sub(r'\[\[([^\]]+)\]\]', r'[\1](\1.md)', content)

# Render markdown with basic frontmatter and content

def render_markdown(data: dict, out_path: str) -> None:
    """
    Render data dict into a markdown file at out_path.
    """
    # Normalize internal wiki links
    data['content'] = normalize_links(data.get('content', ''))
    # Try using Jinja2 template
    env = Environment(loader=FileSystemLoader('templates'))
    try:
        template = env.get_template('analysis.md.j2')
        rendered = template.render(**data)
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(rendered)
        return
    except TemplateNotFound:
        pass
    # Fallback: manual writing with extended frontmatter
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        # Frontmatter
        f.write("---\n")
        f.write(f"title: {data.get('title', '')}\n")
        f.write(f"date: {data.get('date', '')}\n")
        tags = data.get('tags', []) or []
        f.write(f"tags: {', '.join(tags)}\n")
        f.write(f"source: {data.get('source', '')}\n")
        f.write("---\n\n")
        f.write(data.get("content", ""))


# Render HTML with basic template or via Jinja2

def render_html(data: dict, out_path: str) -> None:
    """
    Render data dict into an HTML file at out_path.
    """
    # Normalize internal wiki links
    data['content'] = normalize_links(data.get('content', ''))
    # Try using Jinja2 template
    env = Environment(loader=FileSystemLoader('templates'))
    try:
        template = env.get_template('analysis.html.j2')
        rendered = template.render(**data)
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(rendered)
        return
    except TemplateNotFound:
        pass
    # Fallback: basic HTML
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("<!DOCTYPE html>\n<html>\n<head>\n")
        f.write(f"<title>{data.get('title', '')}</title>\n")
        f.write("</head>\n<body>\n")
        f.write(data.get("content", ""))
        f.write("\n</body>\n</html>")


def main():
    """
    CLI entry point: html_renderer.py (md|html) <data_json> <output_path>
    """
    if len(sys.argv) < 4:
        print("Usage: html_renderer.py (md|html) <data_json> <output_path>")
        sys.exit(1)
    mode = sys.argv[1]
    try:
        data = json.loads(sys.argv[2])
    except json.JSONDecodeError as e:
        print(f"Invalid JSON input: {e}")
        sys.exit(1)
    out_path = sys.argv[3]
    if mode == "md":
        render_markdown(data, out_path)
    elif mode == "html":
        render_html(data, out_path)
    else:
        print(f"Unknown mode: {mode}")
        sys.exit(1)


if __name__ == "__main__":
    main() 