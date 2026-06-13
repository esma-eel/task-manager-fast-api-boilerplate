# Task Manager API

A production-ready Task Management REST API built with **FastAPI**, **PostgreSQL**, **Async SQLAlchemy**, and **JWT Authentication**.

---

## Features

* User registration and authentication
* JWT Access & Refresh Tokens
* CRUD operations for tasks
* Async database operations with SQLAlchemy 2.0
* PostgreSQL database support
* Database migrations with Alembic
* Docker & Docker Compose support
* Interactive API documentation (Swagger & ReDoc)

---

## Tech Stack

| Layer             | Technology                    |
| ----------------- | ----------------------------- |
| Framework         | FastAPI                       |
| Database          | PostgreSQL                    |
| ORM               | SQLAlchemy 2.0 (Async)        |
| Migrations        | Alembic                       |
| Authentication    | JWT (Access + Refresh Tokens) |
| Configuration     | Pydantic Settings             |
| ASGI Server       | Uvicorn                       |
| Production Server | Gunicorn + Uvicorn Workers    |

---

## Prerequisites

Before running the project, make sure you have:

* Python 3.11+
* PostgreSQL (or Docker)
* Docker & Docker Compose
* pip

---

# Local Development Setup

## 1. Clone the Repository

```bash
git clone <repo-url>
cd task-manager
```

## 2. Create and Activate a Virtual Environment

### Linux / macOS

```bash
python -m venv .venv
source .venv/bin/activate
```

### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 4. Configure Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

Update `.env` with your own configuration values.

## 5. Start PostgreSQL

Using Docker:

```bash
docker compose up -d db
```

## 6. Run Database Migrations

```bash
alembic upgrade head
```

## 7. Start the Development Server

```bash
uvicorn app.main:app --reload
```

The application will be available at:

| Service    | URL                         |
| ---------- | --------------------------- |
| API        | http://localhost:8000       |
| Swagger UI | http://localhost:8000/docs  |
| ReDoc      | http://localhost:8000/redoc |

---

## Seed Sample Data (Optional)

```bash
python -m scripts.seed
```

This command creates:

* 10 sample users
* 200 sample tasks

### Default Credentials

| Username | Password   |
| -------- | ---------- |
| user1    | password1  |
| user2    | password2  |
| ...      | ...        |
| user10   | password10 |

---

# Running with Docker

Build and start all services:

```bash
docker compose up --build -d
```

Stop services:

```bash
docker compose down
```

View logs:

```bash
docker compose logs -f
```

---

# Production Deployment

Run using Gunicorn with Uvicorn workers:

```bash
gunicorn app.main:app \
  -w 4 \
  -k uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

### Production Checklist

* Set `DEBUG=False`
* Use a strong `SECRET_KEY`
* Configure HTTPS
* Restrict CORS origins
* Use a managed PostgreSQL instance
* Configure backups and monitoring

---

# Database Migrations

### Create a Migration

```bash
alembic revision --autogenerate -m "migration description"
```

### Apply Migrations

```bash
alembic upgrade head
```

### Roll Back One Migration

```bash
alembic downgrade -1
```

### Check Current Revision

```bash
alembic current
```

---

# API Endpoints

## Authentication

| Method | Endpoint         | Description                               |
| ------ | ---------------- | ----------------------------------------- |
| POST   | `/auth/register` | Register a new user                       |
| POST   | `/auth/login`    | Login and receive access & refresh tokens |
| POST   | `/auth/refresh`  | Generate a new access token               |

---

## Tasks

| Method | Endpoint      | Description           |
| ------ | ------------- | --------------------- |
| GET    | `/tasks/`     | Retrieve all tasks    |
| POST   | `/tasks/`     | Create a new task     |
| GET    | `/tasks/{id}` | Retrieve a task by ID |
| PUT    | `/tasks/{id}` | Update a task         |
| DELETE | `/tasks/{id}` | Delete a task         |

---

# Project Structure

```text
.
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   └── routers/
│       ├── auth.py
│       └── tasks.py
│
├── alembic/
│   └── versions/
│
├── scripts/
│   └── seed.py
│
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

---

# Environment Variables

| Variable                      | Description                   | Example                                            |
| ----------------------------- | ----------------------------- | -------------------------------------------------- |
| `DATABASE_URL`                | PostgreSQL connection string  | `postgresql+asyncpg://user:pass@localhost:5432/db` |
| `SECRET_KEY`                  | JWT signing key               | `your-secret-key`                                  |
| `ALGORITHM`                   | JWT algorithm                 | `HS256`                                            |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access token expiration time  | `30`                                               |
| `REFRESH_TOKEN_EXPIRE_DAYS`   | Refresh token expiration time | `7`                                                |

Example:

```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/task_manager

SECRET_KEY=change-me-in-production
ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

---

# License

MIT License

```

Feel free to use, modify, and distribute this project.
```
