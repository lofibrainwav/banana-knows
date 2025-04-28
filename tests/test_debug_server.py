import pytest

from debug_server import app


@pytest.fixture(autouse=True)
def env_vars(monkeypatch):
    # Ensure environment variables are set for tests
    monkeypatch.setenv("SENTRY_DSN", "")
    monkeypatch.setenv("PROMETHEUS_PORT", "8001")
    monkeypatch.setenv("SLACK_WEBHOOK_URL", "")
    # Enable exception propagation in tests
    app.testing = True
    yield


def test_health_endpoint():
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data.get("status") == "ok"


def test_debug_endpoint():
    client = app.test_client()
    response = client.get("/debug")
    assert response.status_code == 200
    data = response.get_json()
    assert "env" in data and "headers" in data


def test_error_endpoint():
    client = app.test_client()
    with pytest.raises(ZeroDivisionError):
        client.get("/error")


def test_metrics_endpoint():
    client = app.test_client()
    response = client.get("/metrics")
    assert response.status_code == 200
    assert b"request_count" in response.data
