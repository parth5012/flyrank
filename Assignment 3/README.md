# Task API (Assignment 3)

A containerized RESTful **Task Management API** built with FastAPI and SQLModel. This assignment deploys the application with a PostgreSQL database backend using Docker Compose.

The API provides CRUD (Create, Read, Update, Delete) operations over a tasks table with automated database initialization and data seeding.

## One-Command Run

To start both the API and database services (rebuilding images and running in the background) with a single command:

```bash
docker compose up --build -d
```

## Environment Configuration (`.env.example`)

The application can read environment variables from a `.env` file. You can configure your local settings by copying the provided example file:

```bash
cp .env.example .env
```

The config settings inside `.env.example` are:

```ini
# Database connection URL
# Use localhost if running the FastAPI application locally outside of Docker
# DATABASE_URL=postgresql+psycopg://postgres:dev@localhost:5432/tasks

# Use db as host when running the FastAPI application inside Docker Compose
DATABASE_URL=postgresql+psycopg://postgres:dev@db:5432/tasks
```

## API Endpoints Table

| Endpoint | Method | Description | Request Body | Status Codes |
|----------|--------|-------------|--------------|--------------|
| `/` | `GET` | Return API metadata and available endpoints | None | `200 OK` |
| `/health` | `GET` | Return health status of the service | None | `200 OK` |
| `/tasks` | `GET` | Return list of all tasks in the database | None | `200 OK` |
| `/tasks` | `POST` | Create a new task in the database | `{"title": "string"}` | `201 Created`, `400 Bad Request` |
| `/tasks/{task_id}` | `GET` | Return a single task by ID | None | `200 OK`, `404 Not Found` |
| `/tasks/{task_id}` | `PUT` | Update a task's title and/or done status | `{"title": "string", "done": bool}` | `200 OK`, `404 Not Found` |
| `/tasks/{task_id}` | `DELETE` | Delete a task from the database by ID | None | `200 OK`, `404 Not Found` |

## Example Curl Output

To fetch the list of tasks from the running API:

```bash
curl http://localhost:3000/tasks
```

Response Output:
```json
[
  {
    "id": 0,
    "title": "Task 0",
    "done": false
  },
  {
    "id": 1,
    "title": "Task 1",
    "done": false
  },
  {
    "id": 2,
    "title": "Task 2",
    "done": false
  }
]
```

## Database Swagger UI & Data Screenshot

Once the services are run, you can access the interactive API docs to view, execute requests, and inspect database state:

- **Swagger UI**: http://localhost:3000/docs
- **ReDoc**: http://localhost:3000/redoc

Below is the Swagger UI API documentation and data interaction screenshot:

![Swagger UI & Database Data Screenshot](swagger-ui.png)
