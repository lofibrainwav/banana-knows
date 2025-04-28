import pytest
import importlib
import os

from fastapi.testclient import TestClient


@pytest.fixture(scope="function")
def client(tmp_path, monkeypatch):
    # Configure temp SQLite via DATABASE_URL
    db_file = tmp_path / "api_test.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_file}")
    # Reload storage modules to pick up new DATABASE_URL
    import scripts.storage.database as db_mod
    importlib.reload(db_mod)
    db_mod.init_db()
    # Reload crud and API modules
    import scripts.storage.crud as crud_mod
    importlib.reload(crud_mod)
    import scripts.api as api_mod
    importlib.reload(api_mod)
    # Create client
    client = TestClient(api_mod.app)
    yield client


def test_create_and_get(client):
    payload = {"source": "src", "tags": ["x"], "embedding": [0.1, 0.2], "summary": "sum"}
    # Create
    res = client.post("/memory/", json=payload)
    assert res.status_code == 201
    data = res.json()
    assert data["id"] > 0
    assert data["source"] == "src"
    # Get
    get_res = client.get(f"/memory/{data['id']}")
    assert get_res.status_code == 200
    get_data = get_res.json()
    assert get_data == data


def test_get_not_found(client):
    res = client.get("/memory/9999")
    assert res.status_code == 404
    assert res.json()["detail"] == "MemoryEntry not found"


def test_list_and_pagination(client):
    # Create 3 entries
    for i in range(3):
        client.post("/memory/", json={"source": f"s{i}", "tags": [], "embedding": [], "summary": f"m{i}"})
    # Default list
    res = client.get("/memory/")
    assert res.status_code == 200
    items = res.json()
    assert len(items) == 3
    # Pagination
    res2 = client.get("/memory/?limit=1&offset=1")
    assert res2.status_code == 200
    page = res2.json()
    assert len(page) == 1
    assert page[0]["summary"] == "m1"


def test_update_and_not_found(client):
    # Create
    res = client.post("/memory/", json={"source": "a", "tags": [], "embedding": [], "summary": "b"})
    eid = res.json()["id"]
    # Update
    upd = client.put(f"/memory/{eid}", json={"summary": "new"})
    assert upd.status_code == 200
    assert upd.json()["summary"] == "new"
    # Update non-existent
    res_nf = client.put("/memory/9999", json={"summary": "x"})
    assert res_nf.status_code == 404
    assert res_nf.json()["detail"] == "MemoryEntry not found"


def test_delete_and_not_found(client):
    # Create
    res = client.post("/memory/", json={"source": "a", "tags": [], "embedding": [], "summary": "b"})
    eid = res.json()["id"]
    # Delete
    del_res = client.delete(f"/memory/{eid}")
    assert del_res.status_code == 204
    # Confirm deletion
    get_res = client.get(f"/memory/{eid}")
    assert get_res.status_code == 404
    # Delete non-existent
    del_nf = client.delete("/memory/9999")
    assert del_nf.status_code == 404


def test_invalid_payloads(client):
    # Missing fields
    res = client.post("/memory/", json={})
    assert res.status_code == 422
    # Invalid types
    res2 = client.put("/memory/1", json={"tags": "notalist"})
    assert res2.status_code == 422 