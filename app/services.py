"""In-memory todo storage and business logic."""

from app.models import Todo, TodoCreate

_todos: dict[int, Todo] = {}
_next_id = 1


def reset() -> None:
    """Drop every todo and restart ids at 1. Used by tests."""
    global _next_id
    _todos.clear()
    _next_id = 1


def list_todos() -> list[Todo]:
    return list(_todos.values())


def create_todo(data: TodoCreate) -> Todo:
    global _next_id
    todo = Todo(id=_next_id, title=data.title, done=False, due_date=data.due_date)
    _todos[_next_id] = todo
    _next_id += 1
    return todo


def toggle_todo(todo_id: int) -> Todo:
    todo = _todos.get(todo_id)
    if todo is None:
        raise KeyError(todo_id)
    todo.done = not todo.done
    return todo


def delete_todo(todo_id: int) -> None:
    if todo_id not in _todos:
        raise KeyError(todo_id)
    del _todos[todo_id]
