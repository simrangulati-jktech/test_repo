"""Tests for in-memory todo service logic."""

from datetime import date

import pytest

from app import services
from app.models import TodoCreate


def test_list_todos_is_empty_at_start():
    assert services.list_todos() == []


def test_create_todo_assigns_incrementing_ids():
    first = services.create_todo(TodoCreate(title="Buy milk"))
    second = services.create_todo(TodoCreate(title="Walk dog"))

    assert first.id == 1
    assert first.title == "Buy milk"
    assert first.done is False
    assert second.id == 2
    assert second.title == "Walk dog"


def test_create_todo_stores_due_date():
    with_due = services.create_todo(TodoCreate(title="Pay rent", due_date="2026-12-01"))
    without_due = services.create_todo(TodoCreate(title="Someday"))

    assert with_due.due_date == date(2026, 12, 1)
    assert without_due.due_date is None


def test_list_todos_returns_items_in_creation_order():
    services.create_todo(TodoCreate(title="One"))
    services.create_todo(TodoCreate(title="Two"))

    titles = [todo.title for todo in services.list_todos()]
    assert titles == ["One", "Two"]


def test_toggle_todo_flips_done_both_ways():
    todo = services.create_todo(TodoCreate(title="Write tests"))

    toggled = services.toggle_todo(todo.id)
    assert toggled.done is True
    assert services.list_todos()[0].done is True

    toggled_back = services.toggle_todo(todo.id)
    assert toggled_back.done is False


def test_toggle_missing_todo_raises_key_error():
    with pytest.raises(KeyError):
        services.toggle_todo(999)


def test_delete_todo_removes_it_and_does_not_reuse_the_id():
    first = services.create_todo(TodoCreate(title="One"))
    services.delete_todo(first.id)

    assert services.list_todos() == []

    second = services.create_todo(TodoCreate(title="Two"))
    assert second.id == 2
    assert [todo.title for todo in services.list_todos()] == ["Two"]


def test_delete_missing_todo_raises_key_error():
    with pytest.raises(KeyError):
        services.delete_todo(999)
