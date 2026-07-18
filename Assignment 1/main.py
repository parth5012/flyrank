from fastapi import FastAPI
from fastapi.responses import Response
from db import TASKS

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)