from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from datetime import date
from typing import List, Optional

from .models import TimeEntry, TimeEntryCreate
from . import store

app = FastAPI(title="HTML Time Tracker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/api/entries", response_model=TimeEntry, status_code=201)
async def create_entry(entry: TimeEntryCreate) -> TimeEntry:
    created = store.add_entry(entry)
    return created


@app.get("/api/entries", response_model=List[TimeEntry])
async def get_entries(
    date: Optional[date] = Query(default=None),
    person: Optional[str] = Query(default=None),
) -> List[TimeEntry]:
    if date is None and (person is None or not person.strip()):
        return store.list_entries()
    return store.filter_entries(date_filter=date, person_filter=person)
