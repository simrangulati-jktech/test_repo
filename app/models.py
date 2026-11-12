"""Pydantic models for todos."""

from pydantic import BaseModel, Field


class TodoCreate(BaseModel):
    title: str = Field(min_length=1)


class Todo(BaseModel):
    id: int
    title: str
    done: bool = False
