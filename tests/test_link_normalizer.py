from scripts.html_renderer import normalize_links

def test_single_link():
    assert normalize_links("See [[Page]]!") == "See [Page](Page.md)!"

def test_multiple_links():
    assert normalize_links("[[One]] and [[Two]].") == "[One](One.md) and [Two](Two.md)."

def test_link_with_hash():
    assert normalize_links("Go to [[Section#Part]].") == "Go to [Section#Part](Section#Part.md)." 