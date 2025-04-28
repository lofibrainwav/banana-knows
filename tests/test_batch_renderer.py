import json
import os
import shutil
import pytest
from scripts.batch_renderer import main

def create_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f)


def test_batch_renderer_end_to_end(tmp_path):
    # Setup input and output directories
    input_dir = tmp_path / 'input'
    vault_dir = tmp_path / 'vault'
    input_dir.mkdir()
    # Valid JSON
    data1 = {"title": "Doc1", "content": "[[Link]] here", "date": "2023-05-01", "tags": ["a","b"], "source": "test"}
    file1 = input_dir / 'doc1.json'
    create_json(file1, data1)
    # Invalid JSON
    bad_file = input_dir / 'bad.json'
    bad_file.write_text('{invalid json}', encoding='utf-8')
    # Run batch renderer
    main([str(input_dir), str(vault_dir)])
    # Check that vault_dir exists and doc1.md and doc1.html are created
    md_path = vault_dir / 'doc1.md'
    html_path = vault_dir / 'doc1.html'
    assert md_path.exists(), f"Markdown file not created: {md_path}"
    assert html_path.exists(), f"HTML file not created: {html_path}"
    # Verify contents
    md_text = md_path.read_text(encoding='utf-8')
    assert 'title: Doc1' in md_text
    assert 'date: 2023-05-01' in md_text
    assert 'tags: a, b' in md_text
    assert 'source: test' in md_text
    assert '[Link](Link.md)' in md_text
    html_text = html_path.read_text(encoding='utf-8')
    assert '<title>Doc1</title>' in html_text
    assert '[Link](Link.md)' in html_text

@pytest.mark.parametrize("invalid_inputs", [[], ['only_one']])
def test_batch_renderer_arg_errors(tmp_path, invalid_inputs, capsys):
    # Calling main without correct args should print usage and exit
    with pytest.raises(SystemExit):
        main(invalid_inputs)
    captured = capsys.readouterr()
    assert 'Usage: batch_renderer.py' in captured.out 