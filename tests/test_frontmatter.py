import json
import pytest
from scripts import html_renderer as hr
from jinja2 import TemplateNotFound

# Fake Environment to force fallback
class FakeEnv:
    def __init__(self, loader=None):
        pass
    def get_template(self, name):
        raise TemplateNotFound(name)


def test_frontmatter_template(tmp_path):
    """
    Test that render_markdown includes title, date, tags, source in frontmatter via template.
    """
    data = {
        "title": "FrontTest",
        "content": "Some content",
        "date": "2023-01-01",
        "tags": ["tag1", "tag2"],
        "source": "origin"
    }
    out = tmp_path / "front.md"
    hr.render_markdown(data, str(out))
    text = out.read_text(encoding="utf-8").splitlines()
    assert text[0] == '---'
    assert text[1] == 'title: FrontTest'
    assert text[2] == 'date: 2023-01-01'
    assert text[3] == 'tags: tag1, tag2'
    assert text[4] == 'source: origin'
    assert text[5] == '---'


def test_frontmatter_fallback(tmp_path, monkeypatch):
    """
    Test fallback manual frontmatter when template not found.
    """
    data = {
        "title": "FallTest",
        "content": "Fallback content",
        "date": "2024-12-31",
        "tags": ["x", "y"],
        "source": "fallback"
    }
    # Monkeypatch to force TemplateNotFound
    monkeypatch.setattr(hr, 'Environment', FakeEnv)
    out = tmp_path / "fall.md"
    hr.render_markdown(data, str(out))
    text = out.read_text(encoding="utf-8").splitlines()
    assert text[0] == '---'
    assert text[1] == 'title: FallTest'
    assert text[2] == 'date: 2024-12-31'
    assert text[3] == 'tags: x, y'
    assert text[4] == 'source: fallback'
    assert text[5] == '---' 