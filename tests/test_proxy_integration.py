import os
import json
import pytest

import scripts.proxy_integration as proxy_module

@pytest.fixture(autouse=True)
def clear_env(monkeypatch):
    # Ensure no PROXY_SOURCE environment is set
    monkeypatch.delenv('PROXY_SOURCE', raising=False)
    yield
    monkeypatch.delenv('PROXY_SOURCE', raising=False)


def test_load_empty_list(monkeypatch):
    # No PROXY_SOURCE should return empty list
    proxy_list = proxy_module.load_proxy_list()
    assert proxy_list == []


def test_load_comma_list(monkeypatch):
    # Comma-separated list in PROXY_SOURCE
    monkeypatch.setenv('PROXY_SOURCE', 'http://a,http://b')
    lst = proxy_module.load_proxy_list()
    assert lst == ['http://a', 'http://b']


def test_validate_proxy_entry():
    # Validate correct and incorrect formats
    assert proxy_module.validate_proxy_entry('http://ok') is True
    assert proxy_module.validate_proxy_entry('https://ok') is True
    assert proxy_module.validate_proxy_entry('ftp://no') is False


def test_get_proxy_none(monkeypatch):
    # get_proxy should return None when list empty
    proxy = proxy_module.get_proxy()
    assert proxy is None


def test_get_proxy_random(monkeypatch):
    # get_proxy returns one of the available proxies
    monkeypatch.setenv('PROXY_SOURCE', 'http://x,http://y')
    proxy = proxy_module.get_proxy()
    assert proxy in ['http://x', 'http://y'] 