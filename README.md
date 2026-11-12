# Todo

A small FastAPI todo app. Todos live in memory (nothing is written to a database). The page at `/` lets you add, complete, and delete them.

## Setup

Use Python 3.12 or newer. The `python3` on this machine is 3.10.0, which is too old for the installed pytest.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run the app

```bash
source .venv/bin/activate
python -m uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/

## Tests

```bash
source .venv/bin/activate
pytest
```

## Lint

```bash
source .venv/bin/activate
ruff check .
```

## API

- `GET /todos` — list todos
- `POST /todos` — create a todo, JSON body `{"title": "..."}`
- `PATCH /todos/{id}` — toggle `done`
- `DELETE /todos/{id}` — delete a todo
