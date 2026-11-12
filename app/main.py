"""HTTP routes for the todo app."""

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

from app.models import Todo, TodoCreate
from app.services import create_todo, delete_todo, list_todos, toggle_todo

app = FastAPI(title="Todo")

_INDEX_HTML = (Path(__file__).parent / "index.html").read_text(encoding="utf-8")


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    return _INDEX_HTML


@app.get("/todos", response_model=list[Todo])
def get_todos() -> list[Todo]:
    return list_todos()


@app.post("/todos", response_model=Todo, status_code=201)
def post_todo(body: TodoCreate) -> Todo:
    return create_todo(body)


@app.patch("/todos/{todo_id}", response_model=Todo)
def patch_todo(todo_id: int) -> Todo:
    try:
        return toggle_todo(todo_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Todo not found") from None


@app.delete("/todos/{todo_id}", status_code=204)
def remove_todo(todo_id: int) -> None:
    try:
        delete_todo(todo_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Todo not found") from None
