#!/usr/bin/env python3
"""
scripts/fetch_transcript.py

Fetch YouTube transcripts via youtube-transcript-api with proxy support.
Implements logging, retry with exponential backoff, proxy rotation, and fallback.
"""
import logging
import os
import random
import sys
import time

from dotenv import load_dotenv
from youtube_transcript_api import (
    NoTranscriptFound,
    TranscriptsDisabled,
    VideoUnavailable,
    YouTubeTranscriptApi,
)

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger("fetch_transcript")
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(fmt="%(asctime)s %(levelname)s %(message)s")
handler.setFormatter(formatter)
logger.setLevel(logging.INFO)
logger.addHandler(handler)

MAX_RETRIES = int(os.getenv("MAX_RETRIES", "5"))
INITIAL_BACKOFF = float(os.getenv("INITIAL_BACKOFF", "1"))


# Rotate proxy selection
def rotate_proxy():
    # Dynamically read proxy list from environment
    proxy_list = os.getenv("PROXY_LIST", "")
    proxies = [p.strip() for p in proxy_list.split(",") if p.strip()]
    if not proxies:
        return None
    return random.choice(proxies)


# Fetch transcript with retries and fallback
def fetch_transcript(video_id, languages=None):
    attempt = 0
    backoff = INITIAL_BACKOFF
    last_exc = None

    while attempt < MAX_RETRIES:
        proxy_url = rotate_proxy()
        if proxy_url:
            os.environ.update({"HTTP_PROXY": proxy_url, "HTTPS_PROXY": proxy_url})
            logger.info(f"Using proxy: {proxy_url}")
        else:
            os.environ.pop("HTTP_PROXY", None)
            os.environ.pop("HTTPS_PROXY", None)
            logger.info("No proxy: using direct connection")

        try:
            logger.info(f"Fetching transcript for {video_id} (attempt {attempt+1})")
            transcript = (
                YouTubeTranscriptApi.get_transcript(video_id, languages=languages)
                if languages
                else YouTubeTranscriptApi.get_transcript(video_id)
            )
            logger.info("Transcript fetched successfully")
            return transcript
        except (TranscriptsDisabled, NoTranscriptFound, VideoUnavailable) as e:
            logger.error(f"Transcript not available: {e}")
            last_exc = e
            break
        except Exception as e:
            last_exc = e
            status = getattr(e, "status_code", None)
            logger.warning(f"Error: {e} (status={status}); retry in {backoff}s")
            time.sleep(backoff)
            backoff *= 2
            attempt += 1

    # Fallback without proxy
    try:
        logger.info("Attempting fallback without proxy")
        os.environ.pop("HTTP_PROXY", None)
        os.environ.pop("HTTPS_PROXY", None)
        fallback = YouTubeTranscriptApi.get_transcript(video_id)
        logger.info("Fallback succeeded")
        return fallback
    except Exception as e:
        logger.error(f"Fallback failed: {e}")
        raise last_exc or e


# Entry point for CLI
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: fetch_transcript.py VIDEO_ID [LANG1 LANG2 ...]")
        sys.exit(1)
    vid = sys.argv[1]
    langs = sys.argv[2:] if len(sys.argv) > 2 else None
    result = fetch_transcript(vid, languages=langs)
    print(result)
