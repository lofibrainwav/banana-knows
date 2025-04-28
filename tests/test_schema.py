import os
import pytest
from importlib import reload

# Test that init_db() creates the memory_entries table with correct columns

def test_schema_created(tmp_path, monkeypatch):
    # Point DATABASE_URL to a temp SQLite file
    db_file = tmp_path / "test.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_file}")

    # Reload database module to pick up new env var
    import scripts.storage.database as db_mod
    reload(db_mod)
    # Initialize DB (create tables)
    db_mod.init_db()

    # Inspect tables
    from sqlalchemy import inspect
    inspector = inspect(db_mod.engine)
    tables = inspector.get_table_names()
    assert 'memory_entries' in tables

    # Check columns
    cols = [col['name'] for col in inspector.get_columns('memory_entries')]
    expected = {'id', 'timestamp', 'source', 'tags', 'embedding', 'summary'}
    assert expected.issubset(set(cols)) 