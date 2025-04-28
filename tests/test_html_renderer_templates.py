import json
from scripts import html_renderer as hr

def test_markdown_template(tmp_path):
    # Ensure template-based rendering produces expected output
    data = {"title": "TempTest", "content": "RenderContent"}
    out = tmp_path / "temp.md"
    hr.render_markdown(data, str(out))
    text = out.read_text(encoding="utf-8").strip()
    expected = f"---\ntitle: {data['title']}\n---\n\n{data['content']}"
    assert text == expected


def test_html_template(tmp_path):
    data = {"title": "TempHTML", "content": "<div>Content</div>"}
    out = tmp_path / "temp.html"
    hr.render_html(data, str(out))
    text = out.read_text(encoding="utf-8").strip()
    # Check basic HTML structure and title
    assert text.startswith("<!DOCTYPE html>")
    assert f"<title>{data['title']}</title>" in text
    assert data['content'] in text 