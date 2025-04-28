import json
import os
import sys
from scripts import html_renderer as hr


def test_render_markdown(tmp_path):
    data = {"title": "Foo", "content": "Bar"}
    out = tmp_path / "foo.md"
    hr.render_markdown(data, str(out))
    text = out.read_text(encoding="utf-8")
    # Expect extended frontmatter with empty date, tags, source
    expected = "---\ntitle: Foo\ndate: \ntags: \nsource: \n---\n\nBar"
    assert text.strip() == expected


def test_render_html(tmp_path):
    data = {"title": "Foo", "content": "<p>Bar</p>"}
    out = tmp_path / "foo.html"
    hr.render_html(data, str(out))
    text = out.read_text(encoding="utf-8")
    assert "<title>Foo</title>" in text
    assert "<p>Bar</p>" in text


def test_cli_modes(tmp_path, monkeypatch):
    data = {"title": "CLI", "content": "Test"}
    json_str = json.dumps(data)
    # Markdown mode
    out_md = tmp_path / "cli.md"
    monkeypatch.setattr(sys, "argv", ["html_renderer.py", "md", json_str, str(out_md)])
    hr.main()
    text_md = out_md.read_text(encoding="utf-8")
    assert "title: CLI" in text_md

    # HTML mode
    out_html = tmp_path / "cli.html"
    monkeypatch.setattr(sys, "argv", ["html_renderer.py", "html", json_str, str(out_html)])
    hr.main()
    text_html = out_html.read_text(encoding="utf-8")
    assert "<title>CLI</title>" in text_html 