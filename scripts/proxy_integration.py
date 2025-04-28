#!/usr/bin/env python3
"""
scripts/proxy_integration.py

Manage Webshare proxy list: load from config, refresh list, validate, and select proxies.
Includes logging, Prometheus metrics for refreshes and validation errors.
"""
import os
import json
import logging
import random
import requests
from dotenv import load_dotenv
from prometheus_client import Counter

# Load environment variables
load_dotenv()

# Logging configuration
logger = logging.getLogger("proxy_integration")
handler = logging.StreamHandler()
formatter = logging.Formatter(fmt="%(asctime)s %(levelname)s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Prometheus metrics
PROXY_REFRESH_COUNT = Counter('proxy_refresh_count', 'Number of times proxy list refreshed')
PROXY_VALIDATION_ERRORS = Counter('proxy_validation_errors', 'Number of proxy validation errors')

# Config is read dynamically from environment


def load_proxy_list():
    """Load a list of proxies from PROXY_SOURCE environment variable.

    Accepts:
    - Comma-separated list of proxy URLs.
    - A URL returning JSON list.
    - A local JSON file path.
    """
    source = os.getenv('PROXY_SOURCE', '')
    if not source:
        logger.warning('No PROXY_SOURCE configured')
        return []

    # Comma-separated list: split and return
    if ',' in source:
        parts = [p.strip() for p in source.split(',') if p.strip()]
        return [p for p in parts if validate_proxy_entry(p)]
    # Single entry: could be URL, file path, or single proxy
    try:
        if source.startswith('http://') or source.startswith('https://'):
            response = requests.get(source)
            response.raise_for_status()
            data = response.json()
        elif os.path.exists(source):
            with open(source, 'r') as f:
                data = json.load(f)
        else:
            # Single proxy entry
            data = [source]
        return [p for p in data if validate_proxy_entry(p)]
    except Exception as e:
        logger.error(f'Failed to load proxy list: {e}')
        PROXY_VALIDATION_ERRORS.inc()
        return []


def refresh_proxy_list():
    """Refresh proxy list and return new list"""
    PROXY_REFRESH_COUNT.inc()
    return load_proxy_list()


def validate_proxy_entry(proxy):
    """Validate a proxy entry format"""
    try:
        # Simple validation: must start with http:// or https://
        valid = proxy.startswith('http://') or proxy.startswith('https://')
        if not valid:
            PROXY_VALIDATION_ERRORS.inc()
        return valid
    except Exception:
        PROXY_VALIDATION_ERRORS.inc()
        return False


def get_proxy():
    """Return a random proxy from the loaded list"""
    proxies = load_proxy_list()
    if not proxies:
        logger.info('Proxy list empty, returning None')
        return None
    proxy = random.choice(proxies)
    logger.info(f'Selected proxy: {proxy}')
    return proxy


if __name__ == '__main__':
    print(load_proxy_list()) 