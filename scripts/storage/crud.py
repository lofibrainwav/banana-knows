from sqlalchemy.orm import Session
from scripts.storage.models import MemoryEntry


class MemoryEntryNotFound(Exception):
    """Raised when a memory entry is not found in the database."""
    pass


def create_entry(session: Session, data: dict) -> MemoryEntry:
    """
    Create a new MemoryEntry in the database.

    Args:
        session (Session): SQLAlchemy session.
        data (dict): Mapping with keys 'source', 'tags', 'embedding', 'summary'.

    Returns:
        MemoryEntry: The created memory entry.
    """
    entry = MemoryEntry(**data)
    session.add(entry)
    session.commit()
    session.refresh(entry)
    return entry


def get_entry(session: Session, entry_id: int) -> MemoryEntry:
    """
    Retrieve a MemoryEntry by its ID.

    Args:
        session (Session): SQLAlchemy session.
        entry_id (int): ID of the entry to retrieve.

    Returns:
        MemoryEntry: The requested memory entry.

    Raises:
        MemoryEntryNotFound: If no entry exists with the given ID.
    """
    entry = session.query(MemoryEntry).filter(MemoryEntry.id == entry_id).first()
    if entry is None:
        raise MemoryEntryNotFound(f"MemoryEntry with id {entry_id} not found")
    return entry


def list_entries(session: Session, limit: int = 100, offset: int = 0) -> list[MemoryEntry]:
    """
    List memory entries with pagination.

    Args:
        session (Session): SQLAlchemy session.
        limit (int): Maximum number of entries to return.
        offset (int): Number of entries to skip.

    Returns:
        list[MemoryEntry]: List of memory entries.
    """
    return session.query(MemoryEntry).offset(offset).limit(limit).all()


def update_entry(session: Session, entry_id: int, data: dict) -> MemoryEntry:
    """
    Update fields of an existing MemoryEntry.

    Args:
        session (Session): SQLAlchemy session.
        entry_id (int): ID of the entry to update.
        data (dict): Fields to update (subset of 'source', 'tags', 'embedding', 'summary').

    Returns:
        MemoryEntry: The updated memory entry.

    Raises:
        MemoryEntryNotFound: If no entry exists with the given ID.
    """
    entry = get_entry(session, entry_id)
    for key, value in data.items():
        if hasattr(entry, key):
            setattr(entry, key, value)
    session.commit()
    session.refresh(entry)
    return entry


def delete_entry(session: Session, entry_id: int) -> None:
    """
    Delete a MemoryEntry from the database.

    Args:
        session (Session): SQLAlchemy session.
        entry_id (int): ID of the entry to delete.

    Raises:
        MemoryEntryNotFound: If no entry exists with the given ID.
    """
    entry = get_entry(session, entry_id)
    session.delete(entry)
    session.commit()