import os
import pytest
import importlib

from scripts.storage import crud
from scripts.storage.models import MemoryEntry


@pytest.fixture(scope="function")
def db_session(tmp_path, monkeypatch):
    # configure a temporary SQLite database via DATABASE_URL
    db_file = tmp_path / "test.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_file}")
    # reload database module to pick up new DATABASE_URL
    import scripts.storage.database as db_mod
    importlib.reload(db_mod)
    # initialize database (create tables)
    db_mod.init_db()

    # provide a session for tests
    session = db_mod.SessionLocal()
    yield session
    session.close()


def test_create_entry(db_session):
    data = {"source": "test_src", "tags": ["a", "b"], "embedding": [1.0, 2.0], "summary": "test_summary"}
    entry = crud.create_entry(db_session, data)
    assert isinstance(entry, MemoryEntry)
    assert entry.id is not None
    assert entry.source == data["source"]
    assert entry.tags == data["tags"]
    assert entry.embedding == data["embedding"]
    assert entry.summary == data["summary"]


def test_get_entry_exists(db_session):
    data = {"source": "src", "tags": [], "embedding": [], "summary": "sum"}
    created = crud.create_entry(db_session, data)
    fetched = crud.get_entry(db_session, created.id)
    assert fetched.id == created.id
    assert fetched.source == created.source


def test_get_entry_not_found(db_session):
    with pytest.raises(crud.MemoryEntryNotFound):
        crud.get_entry(db_session, 999)


def test_list_entries_pagination(db_session):
    # create 5 entries
    for i in range(5):
        crud.create_entry(db_session, {"source": f"s{i}", "tags": [], "embedding": [], "summary": f"m{i}"})
    entries = crud.list_entries(db_session, limit=2, offset=1)
    assert len(entries) == 2
    assert entries[0].summary == "m1"
    assert entries[1].summary == "m2"


def test_update_entry(db_session):
    data = {"source": "old", "tags": [], "embedding": [], "summary": "old_sum"}
    created = crud.create_entry(db_session, data)
    updated = crud.update_entry(db_session, created.id, {"summary": "new_sum", "source": "new_src"})
    assert updated.id == created.id
    assert updated.summary == "new_sum"
    assert updated.source == "new_src"


def test_update_entry_not_found(db_session):
    with pytest.raises(crud.MemoryEntryNotFound):
        crud.update_entry(db_session, 1234, {"summary": "x"})


def test_delete_entry(db_session):
    data = {"source": "x", "tags": [], "embedding": [], "summary": "y"}
    created = crud.create_entry(db_session, data)
    crud.delete_entry(db_session, created.id)
    with pytest.raises(crud.MemoryEntryNotFound):
        crud.get_entry(db_session, created.id)


def test_delete_entry_not_found(db_session):
    with pytest.raises(crud.MemoryEntryNotFound):
        crud.delete_entry(db_session, 999) 