# Contributing

Thanks for contributing to metadata-service.

## Setup

```bash
cp .env.example .env   # set METADATA_ADMIN_PASSWORD (never commit .env)
cd backend && pip install -r requirements.txt ruff mypy
```

## Workflow

1. Branch from `main`: `feat/<name>` or `fix/<name>`
2. Make focused commits with conventional messages:
   `feat:`, `fix:`, `refactor:`, `docs:`, `test:`, `chore:`
3. Run the gates before pushing:

```bash
cd backend
ruff check app tests
ruff format --check app tests
mypy app
pytest tests -q
```

4. Open a PR against `main` (use the PR template)

## Conventions

- API changes: add typed Pydantic response models; document in README +
  `docs/INTEGRATION.md`
- Status values come from `app/constants.py` — never inline new literals
- Errors use `APIError(status, code, message)` with a stable `code`
- Never commit `.env` or secrets; rotate anything leaked
- Behavior change + refactor = separate commits
