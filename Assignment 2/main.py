from fastapi import FastAPI
from fastapi.responses import Response
from contextlib import asynccontextmanager
from db import create_db_and_tables, Session
from db.models import Task

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
def get_tasks():
    """Return a list of all tasks."""
    return TASKS

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    """Return a single task by its ID, or 404 if not found."""
    for task in TASKS:
        if task["id"] == task_id:
            return task
    return Response(status_code=404,content={ "error": "Task 99 not found" })

@app.post('/tasks')
def create_task(task: dict):
    """Create a new task from the provided title."""
    global next_id
    title = task.get("title")
    if not title:
        return Response(status_code=400, content={ "error": "Title is required" })
    new_task = { "id": next_id, "title": title, "done": False }
    next_id += 1
    TASKS.append(new_task)
    return Response(status_code=201, content="Created")

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: dict):
    """Update an existing task's title and/or done status by ID."""
    if task.get("title") or task.get("done") is not None:
        for i, t in enumerate(TASKS):
            if t["id"] == task_id:
                TASKS[i] = { "id": task_id, "title": task.get("title") if task.get("title") else t["title"], "done": task.get("done", False) }
                return Response(status_code=200, content=TASKS[i])
        return Response(status_code=404, content={ "error": "Task not found" })
    return Response(status_code=400, content={ "error": "No valid fields to update" })

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    """Delete a task by its ID, or 404 if not found."""
    for i, task in enumerate(TASKS):
        if task["id"] == task_id:
            del TASKS[i]
            return Response(status_code=200, content="No Content")
    return Response(status_code=404, content={ "error": "Task not found" })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)