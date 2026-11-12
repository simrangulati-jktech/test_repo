# Project rules

## Tests and lint

From the repository root, with the virtual environment activated:

```bash
pytest
ruff check .
```

Fix lint and test failures before finishing a change.

## Code style

- Keep the app small and readable. Do not add features that were not asked for.
- Business logic belongs in `app/services.py`.
- HTTP routes belong in `app/main.py`.
- Pydantic models belong in `app/models.py`.
- Use clear names and straightforward control flow.
- Prefer the standard library and the packages already listed in `requirements.txt`.

## Protected files

Do not edit these paths without explicit human approval:

- `.github/`
- `requirements.txt`
