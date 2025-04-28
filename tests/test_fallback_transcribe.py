import os
import pytest

import scripts.fallback_transcribe as fb


def test_check_model_missing(monkeypatch, tmp_path):
    # Set a non-existing model path
    fake_path = tmp_path / "no_model"
    monkeypatch.setenv("FALLBACK_MODEL_PATH", str(fake_path))
    with pytest.raises(FileNotFoundError):
        fb.load_model()


def test_transcribe_with_stub_model(monkeypatch):
    # Stub load_model to return a dummy model
    class DummyModel:
        def translate_batch(self, inputs):
            # Return list of objects with hypotheses list
            return [type("Res", (), {"hypotheses": [["token1", "token2"]]})()]

    monkeypatch.setenv("FALLBACK_MODEL_PATH", "./models/whisper")
    monkeypatch.setattr(fb, "load_model", lambda: DummyModel())
    text = fb.transcribe("dummy_input")
    assert text == "token1token2" 