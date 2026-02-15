# Travel Planner API

A RESTful API for managing travel projects and collecting desired places to visit, powered by the [Art Institute of Chicago API](https://api.artic.edu/docs/).

Built with **FastAPI**, **PostgreSQL**, **SQLAlchemy 2.x** (async), and **Alembic**.

---

## Quick Start

### Prerequisites

- Docker & Docker Compose

### Run

```bash
git clone <repo-url> && cd ta_develops_today
cp .env.example .env  # or use the existing .env
docker-compose up --build
```

The API will be available at `http://localhost:8000`.

### API Documentation

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `DATABASE_URL` | `postgresql+asyncpg://postgres:postgres@postgres:5432/travel_planner` | Async database connection string |
| `ARTIC_API_BASE_URL` | `https://api.artic.edu/api/v1` | Art Institute of Chicago API base URL |

---

## API Endpoints

### Projects

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/projects/` | Create a project with 1–10 places |
| `GET` | `/api/v1/projects/` | List all projects |
| `GET` | `/api/v1/projects/{id}` | Get project details with places |
| `PUT` | `/api/v1/projects/{id}` | Update project info |
| `DELETE` | `/api/v1/projects/{id}` | Delete project (blocked if any place visited) |

### Places

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/projects/{id}/places` | Add a place to a project |
| `GET` | `/api/v1/projects/{id}/places` | List all places in a project |
| `GET` | `/api/v1/projects/{id}/places/{place_id}` | Get a single place |
| `PATCH` | `/api/v1/projects/{id}/places/{place_id}` | Update notes / mark as visited |

---

## Example Requests

### Create a project with places

```bash
curl -X POST http://localhost:8000/api/v1/projects/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Paris Art Tour",
    "description": "Must-see artworks",
    "start_date": "2026-06-01",
    "places": [
      {"external_id": 111317},
      {"external_id": 111060}
    ]
  }'
```

### Add a place to an existing project

```bash
curl -X POST http://localhost:8000/api/v1/projects/1/places \
  -H "Content-Type: application/json" \
  -d '{"external_id": 27992}'
```

### Update notes and mark visited

```bash
curl -X PATCH http://localhost:8000/api/v1/projects/1/places/1 \
  -H "Content-Type: application/json" \
  -d '{"notes": "Beautiful painting!", "visited": true}'
```

---

## Business Rules

- Each project must have **1–10 places**
- Places are validated against the **Art Institute of Chicago API** before being stored
- **No duplicate** external places within the same project
- A project **cannot be deleted** if any of its places are marked as visited
- A project is automatically marked as **completed** when all its places are visited

---

## Project Structure

```
├── main.py                    # FastAPI app entrypoint
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── alembic/                   # Database migrations
├── src/
│   ├── config.py              # Settings (pydantic-settings)
│   ├── dependencies.py        # FastAPI dependencies
│   ├── db/
│   │   ├── base.py            # SQLAlchemy DeclarativeBase
│   │   └── session.py         # Async engine & session
│   ├── tables/
│   │   ├── mixins.py          # TimeMixin (created_at, updated_at)
│   │   ├── project.py         # Project model
│   │   └── project_place.py   # ProjectPlace model
│   ├── schemas/
│   │   ├── project.py         # Request/response schemas
│   │   └── place.py
│   ├── services/
│   │   ├── artic_service.py   # Art Institute API client
│   │   └── db_service.py      # Database CRUD operations
│   └── api/
│       ├── projects.py        # Project endpoints
│       ├── places.py          # Place endpoints
│       └── routers.py         # Central router
```

---

## Database Migrations

```bash
# Generate a new migration
docker-compose exec backend alembic revision --autogenerate -m "description"

# Apply migrations
docker-compose exec backend alembic upgrade head

# Rollback one step
docker-compose exec backend alembic downgrade -1
```

---

## Tech Stack

- **FastAPI** — async web framework
- **SQLAlchemy 2.x** — async ORM with `Mapped` type annotations
- **PostgreSQL** — relational database
- **Alembic** — database migrations
- **Pydantic v2** — request/response validation
- **httpx** — async HTTP client for third-party API
- **Docker Compose** — containerized local development
