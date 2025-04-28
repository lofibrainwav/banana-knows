import os

import pytest

import scripts.fetch_transcript as fetch_module


@pytest.fixture(autouse=True)
def setup_env(monkeypatch):
    # Fast backoff and minimal retries for tests
    monkeypatch.setenv("INITIAL_BACKOFF", "0")
    monkeypatch.setenv("MAX_RETRIES", "1")
    os.environ.pop("PROXY_LIST", None)
    yield
    os.environ.pop("PROXY_LIST", None)


def test_direct_success(monkeypatch):
    # Stub get_transcript to return sample transcript
    sample = [{"text": "hello", "start": 0, "duration": 1}]

    def stub(video_id, languages=None):
        return sample

    monkeypatch.setattr(fetch_module.YouTubeTranscriptApi, "get_transcript", stub)
    result = fetch_module.fetch_transcript("video123")
    assert result == sample


def test_rotate_proxy(monkeypatch):
    # Test rotate_proxy returns one of the configured proxies
    monkeypatch.setenv('PROXY_LIST', 'http://p1,http://p2')
    proxy = fetch_module.rotate_proxy()
    assert proxy in ['http://p1', 'http://p2']


def test_fetch_sets_http_proxy(monkeypatch):
    # Test that fetch_transcript sets HTTP_PROXY env var when PROXY_LIST provided
    sample = [{'text': 'ok', 'start': 0, 'duration': 1}]
    monkeypatch.setenv('PROXY_LIST', 'http://p1,http://p2')
    monkeypatch.setattr(fetch_module.YouTubeTranscriptApi, 'get_transcript', lambda vid, languages=None: sample)
    fetch_module.fetch_transcript('videoX')
    assert os.environ.get('HTTP_PROXY') in ['http://p1', 'http://p2']
    # Clean up
    os.environ.pop('HTTP_PROXY', None)
    os.environ.pop('HTTPS_PROXY', None)


def test_fallback_error(monkeypatch):
    # Stub to always raise TranscriptsDisabled to trigger fallback and propagation
    def stub_raise(video_id, languages=None):
        raise fetch_module.TranscriptsDisabled("disabled")

    monkeypatch.setattr(fetch_module.YouTubeTranscriptApi, "get_transcript", stub_raise)
    with pytest.raises(fetch_module.TranscriptsDisabled):
        fetch_module.fetch_transcript("videoZ")
