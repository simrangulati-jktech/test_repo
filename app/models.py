"""Pydantic models for todos."""

from datetime import date

from pydantic import BaseModel, Field


class TodoCreate(BaseModel):
    title: str = Field(min_length=1)
    due_date: date | None = None


class Todo(BaseModel):
    id: int
    title: str
    done: bool = False
    due_date: date | None = None
