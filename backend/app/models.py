from datetime import date
from pydantic import BaseModel, field_validator


class TimeEntryBase(BaseModel):
    date: date
    person: str
    team: str
    description: str
    duration_minutes: int

    @field_validator("person", "team", "description")
    @classmethod
    def non_empty_strings(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("must not be empty")
        return v.strip()

    @field_validator("duration_minutes")
    @classmethod
    def positive_duration(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("duration_minutes must be positive")
        return v


class TimeEntryCreate(TimeEntryBase):
    pass


class TimeEntry(TimeEntryBase):
    id: int


class TimeEntryFilter(BaseModel):
    date: date | None = None
    person: str | None = None
