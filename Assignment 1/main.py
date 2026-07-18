from fastapi import FastAPI
from fastapi.responses import Response
from db import TASKS,next_id

app = FastAPI()

@app.get("/")
def root():
    return { "name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }

    
@app.get("/health")
def health():
    return { "status": "ok" }

@app.get("/tasks")
def get_tasks():
    return TASKS

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in TASKS:
        if task["id"] == task_id:
            return task
    return Response(status_code=404,content={ "error": "Task 99 not found" })

@app.post('/tasks')
def create_task(task: dict):
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
    if task.get("title") or task.get("done") is not None:
        for i, t in enumerate(TASKS):
            if t["id"] == task_id:
                TASKS[i] = { "id": task_id, "title": task.get("title") if task.get("title") else t["title"], "done": task.get("done", False) }
                return Response(status_code=200, content=TASKS[i])
        return Response(status_code=404, content={ "error": "Task not found" })
    return Response(status_code=400, content={ "error": "No valid fields to update" })

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for i, task in enumerate(TASKS):
        if task["id"] == task_id:
            del TASKS[i]
            return Response(status_code=200, content="No Content")
    return Response(status_code=404, content={ "error": "Task not found" })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)