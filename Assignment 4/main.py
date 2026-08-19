from fastapi import FastAPI
from fastapi.responses import Response
from contextlib import asynccontextmanager
from db import create_db_and_tables, Session
from db.db import APISession
from db.models import Task
from db.operations import get_all_tasks, get_task_by_id
from db.auth import sign_up, sign_in, sign_out, get_user
import re
from typing import Any


@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- STARTUP LOGIC ---
    print("Uvicorn is starting up... triggering function now!")
    create_db_and_tables()

    yield  # The application runs and handles requests while paused here

    # --- SHUTDOWN LOGIC ---
    print("Uvicorn is shutting down... clean up connections here.")

app = FastAPI(lifespan=lifespan)


@app.get("/")
def root():
    """Return API metadata and available endpoints."""
    return { "name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }


@app.get("/health")
def health():
    """Return the health status of the service."""
    return { "status": "ok" }

@app.get("/tasks")
def get_tasks(session: APISession):
    """Return a list of all tasks."""
    return get_all_tasks(session)

@app.get("/tasks/{task_id}")
def get_task(task_id: int, session: APISession):
    """Return a single task by its ID, or 404 if not found."""
    task = get_task_by_id(session, task_id)
    if task is None:
        return Response(status_code=404, content={ "error": "Task not found" })
    return task

@app.post('/tasks')
def create_task(task: dict, session: APISession):
    """Create a new task from the provided title."""
    title = task.get("title")
    if not title:
        return Response(status_code=400, content={ "error": "Title is required" })
    new_task = Task(title=title)
    session.add(new_task)
    session.commit()
    return Response(status_code=201, content="Created")

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: dict, session: APISession):
    """Update an existing task's title and/or done status by ID."""

    task_to_update = get_task_by_id(session, task_id)
    if task_to_update is None:
        return Response(status_code=404, content={ "error": "Task not found" })
    if task.get("title"):
        task_to_update.title = task["title"]
    if task.get("done") is not None:
        task_to_update.done = task["done"]
    session.commit()
    return task_to_update

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, session: APISession):
    """Delete a task by its ID, or 404 if not found."""
    task_to_delete = get_task_by_id(session, task_id)
    if task_to_delete is None:
        return Response(status_code=404, content={ "error": "Task not found" })
    session.delete(task_to_delete)
    session.commit()
    return Response(status_code=200, content="No Content")

@app.post("/auth/signup")
def signup(user: dict):
    try:
        response = sign_up(**user)
        if response.user:
            return Response(status_code=201, content="No Content")
        return Response(status_code=400, content=response)
    except Exception as e:
        return Response(status_code=500, content=str(e))

@app.post("/auth/login")
def login(user:dict):
    try:
        response = sign_in(**user)
        if response.user:
            content = {
                "access_token": response.access_token,
                "refresh_token": response.refresh_token
            }
            return Response(status_code=200, content=content)
        return Response(status_code=400, content=response)
    except Exception as e:
        return Response(status_code=500, content=str(e))

@app.get("/public/info")
def public_info():
    return Response(status_code=200, content="Welcome stranger! This info is public.")

@app.get("/protected/profile")
def protected_profile(headers: dict[Any,Any]):
    auth_header: str = str(headers.get("Authorization", ""))
    
    # Regex: Match "Bearer <token>" and capture the token
    match = re.match(r'^Bearer\s+(\S+)$', auth_header)
    err = Response(
        status_code=401,
        content='{"error": "Access token required"}',
        media_type="application/json"
    )
    if not match:
        return err
    
    token = match.group(1)  # Extract the token
    user = get_user(token)
    if not user:
        return err
    return Response(status_code=200, content="Welcome! This info is protected.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
