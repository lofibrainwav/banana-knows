#!/usr/bin/env python3
"""
scripts/fallback_transcribe.py

Fallback transcription using CTranslate2-backed faster-whisper/WhisperX.
Includes pre-flight dependency check, model loading, transcription function, and graceful error handling.
"""
import os
import sys
import logging

# Add safe import for ctranslate2
try:
    import ctranslate2
except ImportError:
    ctranslate2 = None

# Configure logging
logger = logging.getLogger("fallback_transcribe")
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(fmt="%(asctime)s %(levelname)s %(message)s")
handler.setFormatter(formatter)
logger.setLevel(logging.INFO)
logger.addHandler(handler)

# Directory for models
MODEL_PATH = os.getenv("FALLBACK_MODEL_PATH", "./models/whisper")

# Pre-flight check for model files
def check_model_exists():
    if not os.path.isdir(MODEL_PATH):
        raise FileNotFoundError(f"Model path not found: {MODEL_PATH}")

# Replace load_model to use dynamic path and proper error for missing folder
def load_model():
    # Ensure ctranslate2 library is available
    if ctranslate2 is None:
        raise ImportError("ctranslate2 library not installed. Please install via requirements.txt.")
    # Determine model path dynamically from environment
    model_path = os.getenv("FALLBACK_MODEL_PATH", MODEL_PATH)
    if not os.path.isdir(model_path):
        raise FileNotFoundError(f"Model path not found: {model_path}")
    try:
        model = ctranslate2.models.WhisperModel(model_path)
        logger.info(f"Loaded model from {model_path}")
        return model
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        raise

# Transcribe audio buffer or file
def transcribe(input_data, model=None):
    if model is None:
        model = load_model()
    try:
        # input_data could be path or numpy array
        logger.info("Starting transcription via fallback model")
        results = model.translate_batch([input_data])
        # results[0] contains tokens and scores; process accordingly
        text = "".join(token for token in results[0].hypotheses[0])
        logger.info("Transcription completed")
        return text
    except Exception as e:
        logger.error(f"Error during fallback transcription: {e}")
        raise

# CLI entry point
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: fallback_transcribe.py <input> [model_path]")
        sys.exit(1)
    input_data = sys.argv[1]
    if len(sys.argv) > 2:
        os.environ["FALLBACK_MODEL_PATH"] = sys.argv[2]
    output = transcribe(input_data)
    print(output) 