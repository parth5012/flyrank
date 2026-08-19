# Task API (Assignment 4)

A containerized RESTful **Task Management API** built with FastAPI and SQLModel, now with **JWT-based authentication and protected endpoints**. This assignment adds user authentication (sign-up, login, logout) with token-based access control using Supabase Auth.

The API provides CRUD (Create, Read, Update, Delete) operations over a tasks table, along with public and protected routes secured via Bearer token authentication.

## One-Command Run

To start both the API and database services (rebuilding images and running in the background) with a single command:

\\\ash
docker compose up --build -d
\\\

## Environment Configuration (\.env.example\)

The application can read environment variables from a \.env\ file. You can configure your local settings by copying the provided example file:

\\\ash
cp .env.example .env
\\\

The config settings inside \.env.example\ are:

\\\ini
# Database connection URL
# Use localhost if running the FastAPI application locally outside of Docker
# DATABASE_URL=postgresql://localhost:5432/tasks

# Use db as host when running the FastAPI application inside Docker Compose
DATABASE_URL=postgresql://db:5432/tasks

# Supabase Auth Configuration
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-key
\\\

## Authentication Flow

### Sign Up
\\\ash
POST /auth/signup
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword"
}
\\\

### Login
\\\ash
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword"
}
\\\

**Response:**
\\\json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "token_string"
}
\\\

### Accessing Protected Routes

Include the Bearer token in the \Authorization\ header:

\\\ash
curl -H "Authorization: Bearer <access_token>" http://localhost:8000/protected/profile
\\\

### Logout
\\\ash
POST /auth/logout
Authorization: Bearer <access_token>
\\\

## API Endpoints Table

| Endpoint | Method | Description | Auth Required | Status Codes |
|----------|--------|-------------|----------------|--------------|
| \/\ | \GET\ | Return API metadata | ❌ No | \200 OK\ |
| \/health\ | \GET\ | Health status | ❌ No | \200 OK\ |
| \/public/info\ | \GET\ | Public information | ❌ No | \200 OK\ |
| \/auth/signup\ | \POST\ | Register new user | ❌ No | \201 Created\, \400 Bad Request\ |
| \/auth/login\ | \POST\ | Login with email/password | ❌ No | \200 OK\, \400 Bad Request\ |
| \/auth/logout\ | \POST\ | Logout (invalidate token) | ✅ **Yes** | \204 No Content\, \401 Unauthorized\ |
| \/protected/profile\ | \GET\ | Get user profile | ✅ **Yes** | \200 OK\, \401 Unauthorized\ |
| \/tasks\ | \GET\ | List all tasks | ❌ No | \200 OK\ |
| \/tasks\ | \POST\ | Create new task | ❌ No | \201 Created\, \400 Bad Request\ |
| \/tasks/{task_id}\ | \GET\ | Get task by ID | ❌ No | \200 OK\, \404 Not Found\ |
| \/tasks/{task_id}\ | \PUT\ | Update task | ❌ No | \200 OK\, \404 Not Found\ |
| \/tasks/{task_id}\ | \DELETE\ | Delete task | ❌ No | \200 OK\, \404 Not Found\ |

## Swagger UI with Authorization

Once the API is running, access the interactive API docs with built-in authentication:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Using the Authorize Button in Swagger

1. Click the **🔒 Authorize** button at the top of the Swagger UI
2. Paste your Bearer token (from login response) in the \Authorization\ field
3. Click **Authorize** — subsequent requests will include the token automatically
4. Protected routes will now execute with authentication

## Example Requests

### Sign Up
\\\ash
curl -X POST http://localhost:8000/auth/signup \\
  -H "Content-Type: application/json" \\
  -d '{"email":"user@example.com","password":"password123"}'
\\\

### Login
\\\ash
curl -X POST http://localhost:8000/auth/login \\
  -H "Content-Type: application/json" \\
  -d '{"email":"user@example.com","password":"password123"}'
\\\

### Access Protected Route
\\\ash
curl http://localhost:8000/protected/profile \\
  -H "Authorization: Bearer your_access_token_here"
\\\

**Response:**
\\\
Welcome! This info is protected.
\\\

### Logout
\\\ash
curl -X POST http://localhost:8000/auth/logout \\
  -H "Authorization: Bearer your_access_token_here"
\\\

## Security Features

✅ **HTTPBearer Security Scheme** — Swagger UI shows 🔒 padlock on protected routes  
✅ **Bearer Token Validation** — Middleware validates \Authorization: Bearer <token>\ format  
✅ **401 Unauthorized** — Missing, malformed, or invalid tokens return proper error  
✅ **Reusable Guard** — Single \get_user()\ dependency protects multiple routes  
✅ **Supabase Auth Integration** — Leverages Supabase for user management and token verification  

## Architecture

- **FastAPI** — Web framework with automatic OpenAPI/Swagger documentation
- **SQLModel** — SQLAlchemy ORM with Pydantic validation
- **PostgreSQL** — Persistent data store for tasks
- **Supabase Auth** — User authentication and JWT token management
- **HTTPBearer** — FastAPI security scheme for Bearer tokens
- **Docker Compose** — Multi-container orchestration
