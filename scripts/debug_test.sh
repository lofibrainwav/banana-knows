#!/usr/bin/env bash
set -euo pipefail

# URL of the debug server (default to localhost:5000)
URL=${DEBUG_SERVER_URL:-http://localhost:5000}

echo "Testing /health endpoint..."
curl -sf "$URL/health" || { echo "Health check failed"; exit 1; }

echo "Testing /debug endpoint..."
curl -sf "$URL/debug" || { echo "Debug endpoint failed"; exit 1; }

echo "Testing /metrics endpoint..."
curl -sf "$URL/metrics" || { echo "Metrics endpoint failed"; exit 1; }

echo "Testing /error endpoint (should return 500)..."
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$URL/error" || true)
if [ "$HTTP_STATUS" != "500" ]; then
  echo "Error endpoint did not return 500 (returned $HTTP_STATUS)"
  exit 1
fi

echo "All debug server tests passed successfully." 