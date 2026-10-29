# Bottling Inventory System

A backend API for tracking raw materials and bottling production, with an audit history of every stock movement.

## Why I built this

I worked as a production operative at a bottling company. Stock was checked manually once a month or quarter, so the real stock level was unclear in between. I taught myself Python and built this system to track stock in real time instead.

## Features

- Raw material management (spirit, bottles, caps, labels) with current and safety stock levels
- Inbound / outbound stock tracking
- Automatic raw material deduction when production is recorded
- Audit history of stock movements
- Interactive API docs and a health check endpoint


## Tech stack

- Python, FastAPI, Pydantic
- PostgreSQL
- Docker and Docker Compose
- pytest

## Project structure

```
app/
├── api/              # HTTP layer: routes, request/response handling
├── services/         # Business workflows (e.g. production -> stock deduction -> audit log)
├── domain/           # Core models and rules
├── infrastructure/   # Database access
├── core/             # Configuration
└── main.py           # App entry point
tests/
```

I used a layered architecture inspired by Clean Architecture, so business rules are kept separate from the web framework and database. This makes them easier to test and change.

## Getting started

### With Docker

```bash
docker compose up --build
```

### Without Docker

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
# create a .env file with your settings (see .env.example if provided)
python create_tables.py
uvicorn app.main:app --reload
```

Then open:

- API docs: http://localhost:8000/docs
- Health check: http://localhost:8000/health

All API routes are under `/api/v1`.

## Running tests

```bash
pytest
```

## Notes

- All data in this repository is sample data and does not come from any real company.
- CORS is currently open for development and should be restricted in production.

## Future improvements

- Warning system when the raw material is low
