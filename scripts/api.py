from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from scripts.storage.database import SessionLocal, init_db
from scripts.storage.crud import (
    create_entry,
    get_entry,
    list_entries,
    update_entry,
    delete_entry,
    MemoryEntryNotFound,
)

app = FastAPI()


@app.on_event("startup")
def on_startup():
    init_db()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class MemoryEntryCreate(BaseModel):
    source: str
    tags: List[str]
    embedding: List[float]
    summary: str


class MemoryEntryUpdate(BaseModel):
    source: Optional[str] = None
    tags: Optional[List[str]] = None
    embedding: Optional[List[float]] = None
    summary: Optional[str] = None


class MemoryEntrySchema(BaseModel):
    id: int
    timestamp: datetime
    source: str
    tags: List[str]
    embedding: List[float]
    summary: str

    class Config:
        orm_mode = True


@app.post("/memory/", response_model=MemoryEntrySchema, status_code=201)
def api_create(entry: MemoryEntryCreate, db: Session = Depends(get_db)):
    return create_entry(db, entry.dict())


@app.get("/memory/{entry_id}", response_model=MemoryEntrySchema)
def api_get(entry_id: int, db: Session = Depends(get_db)):
    try:
        return get_entry(db, entry_id)
    except MemoryEntryNotFound:
        raise HTTPException(status_code=404, detail="MemoryEntry not found")


@app.get("/memory/", response_model=List[MemoryEntrySchema])
def api_list(limit: int = 100, offset: int = 0, db: Session = Depends(get_db)):
    return list_entries(db, limit, offset)


@app.put("/memory/{entry_id}", response_model=MemoryEntrySchema)
def api_update(entry_id: int, entry: MemoryEntryUpdate, db: Session = Depends(get_db)):
    try:
        return update_entry(db, entry_id, entry.dict(exclude_unset=True))
    except MemoryEntryNotFound:
        raise HTTPException(status_code=404, detail="MemoryEntry not found")


@app.delete("/memory/{entry_id}", status_code=204)
def api_delete(entry_id: int, db: Session = Depends(get_db)):
    try:
        delete_entry(db, entry_id)
    except MemoryEntryNotFound:
        raise HTTPException(status_code=404, detail="MemoryEntry not found") 