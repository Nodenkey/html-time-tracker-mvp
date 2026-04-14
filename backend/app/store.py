from __future__ import annotations

from datetime import date
from typing import List, Optional

from .models import TimeEntry, TimeEntryCreate


# In-memory store: simple list of dict-like TimeEntry objects
_entries: List[TimeEntry] = []
_next_id: int = 1


def _seed_data() -> None:
    global _entries, _next_id
    if _entries:
        return
    seed_items = [
        TimeEntry(id=1, date=date(2026, 4, 13), person="Sara Gordic", team="Platform", description="Sprint planning and backlog refinement", duration_minutes=90),
        TimeEntry(id=2, date=date(2026, 4, 13), person="Sara Gordic", team="Platform", description="Implement POST /entries backend", duration_minutes=120),
        TimeEntry(id=3, date=date(2026, 4, 14), person="Samuel Sackey", team="Frontend", description="Build HTML time entry form", duration_minutes=180),
    ]
    _entries.extend(seed_items)
    _next_id = len(_entries) + 1


_seed_data()


def list_entries() -> List[TimeEntry]:
    return list(_entries)


def add_entry(payload: TimeEntryCreate) -> TimeEntry:
    global _next_id
    entry = TimeEntry(id=_next_id, **payload.model_dict())
    _entries.append(entry)
    _next_id += 1
    return entry


def filter_entries(*, date_filter: Optional[date] = None, person_filter: Optional[str] = None) -> List[TimeEntry]:
    results = _entries
    if date_filter is not None:
        results = [e for e in results if e.date == date_filter]
    if person_filter is not None:
        lowered = person_filter.strip().lower()
        results = [e for e in results if e.person.lower() == lowered]
    return list(results)


def clear_entries() -> None:
    """Utility for tests to reset store to seed state."""
    global _entries, _next_id
    _entries = []
    _next_id = 1
    _seed_data()
