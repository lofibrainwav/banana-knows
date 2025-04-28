import json
import logging
import os

import requests
import sentry_sdk
from dotenv import load_dotenv
from flask import Flask, Response, jsonify, request
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    Counter,
    generate_latest,
    start_http_server,
)

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Sentry integration
SENTRY_DSN = os.getenv("SENTRY_DSN")
if SENTRY_DSN:
    sentry_sdk.init(dsn=SENTRY_DSN, traces_sample_rate=1.0)

# Structured JSON logging
logger = logging.getLogger("debug_server")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    json.dumps(
        {
            "timestamp": "%(asctime)s",
            "level": "%(levelname)s",
            "stage": "debug",
            "message": "%(message)s",
        }
    )
)
handler.setFormatter(formatter)
logger.addHandler(handler)

# Prometheus metrics
REQUEST_COUNT = Counter(
    "request_count", "Total HTTP Requests", ["method", "endpoint", "http_status"]
)
# Start Prometheus metrics server
prometheus_port = int(os.getenv("PROMETHEUS_PORT", "8001"))
start_http_server(prometheus_port)

# Slack notifications
SLACK_WEBHOOK = os.getenv("SLACK_WEBHOOK_URL")


def notify_slack(message: str):
    if SLACK_WEBHOOK:
        try:
            requests.post(SLACK_WEBHOOK, json={"text": message})
        except Exception as e:
            logger.error(f"Slack notify failed: {e}")


# Health check endpoint
@app.route("/health", methods=["GET"])
def health():
    REQUEST_COUNT.labels(method="GET", endpoint="/health", http_status="200").inc()
    logger.info("Health check ok")
    return jsonify({"status": "ok"}), 200


# Debug info endpoint
@app.route("/debug", methods=["GET"])
def debug():
    data = {
        "env": {
            k: v
            for k, v in os.environ.items()
            if k in ["SENTRY_DSN", "PROMETHEUS_PORT"]
        },
        "headers": dict(request.headers),
    }
    REQUEST_COUNT.labels(method="GET", endpoint="/debug", http_status="200").inc()
    logger.info("Debug info delivered")
    return jsonify(data), 200


# Intentional error endpoint to test Sentry and Slack
@app.route("/error", methods=["GET"])
def error_test():
    try:
        1 / 0
    except Exception as e:
        logger.error("Intentional error occurred", exc_info=True)
        notify_slack(f"Error occurred: {e}")
        raise


# Prometheus metrics endpoint
@app.route("/metrics", methods=["GET"])
def metrics():
    REQUEST_COUNT.labels(method="GET", endpoint="/metrics", http_status="200").inc()
    data = generate_latest()
    return Response(data, mimetype=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    port = int(os.getenv("DEBUG_SERVER_PORT", "5000"))
    logger.info(f"Starting debug server on port {port}")
    app.run(host="0.0.0.0", port=port)
