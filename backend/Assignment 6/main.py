from fastapi import FastAPI,Depends
from fastapi.responses import Response
from contextlib import asynccontextmanager
from pydantic import ValidationError
from db import create_db_and_tables, Session
from db.db import APISession
from db.models import Task
from db.operations import get_all_tasks, get_task_by_id
from db.auth import sign_up, sign_in, sign_out
from llm.schema import ChatResponse,ChatRequest
from llm.utils import client
from prompts.chat_v1 import SYSTEM_PROMPT
from utils.retries import call_with_retry
from utils.dependencies import get_user
from utils.parse import format_json
import re
import json
import pathlib
import datetime
from config import Settings
from fastapi import Request
from fastapi.responses import JSONResponse



settings = Settings()

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
def protected_profile(user = Depends(get_user)):
    return Response(status_code=200, content="Welcome! This info is protected.")

@app.post("/auth/logout")
def logout(user = Depends(get_user)):
    sign_out()
    return Response(status_code=204, content="")
@app.post("/classify")
@app.post("/chat")
async def chat(request: Request):
    try:
        data = await request.json()
    except Exception:
        return JSONResponse(status_code=400, content={"detail": "Invalid JSON", "field": "text"})
    try:
        validated = ChatRequest(**data)
    except ValidationError as e:
        field = e.errors()[0]["loc"][0] if e.errors() else "text"
        return JSONResponse(status_code=400, content={"detail": e.errors(), "field": str(field)})

    # kill switch — must be before any model call
    if not settings.LLM_ENABLED:
        fallback = ChatResponse(category="other", urgency="normal", confidence=0.0, reason="LLM disabled via kill switch")
        return JSONResponse(status_code=503, content=fallback.model_dump())

    if settings.LLM_STUB:
        stub = ChatResponse(category="other", urgency="normal", confidence=0.5, reason="Stub classification")
        return JSONResponse(status_code=200, content=stub.model_dump())

    def _log_call(model: str, usage, duration_ms: int, repair: bool):
        pathlib.Path("logs").mkdir(parents=True, exist_ok=True)
        line = {"prompt_version": "chat-v1", "model": model, "input_tokens": getattr(usage, "prompt_tokens", 0) if usage else 0, "output_tokens": getattr(usage, "completion_tokens", 0) if usage else 0, "duration_ms": duration_ms, "repair": repair}
        with open("logs/llm_calls.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(line) + "\n")

    def _parse_and_validate(raw: str):
        """Step 1+2: strip fence via format_json, JSON.parse, Pydantic validate."""
        extracted = format_json(raw)
        obj = json.loads(extracted)
        return ChatResponse.model_validate(obj)

    def _quarantine(raw: str, raw2: str | None, error: str):
        pathlib.Path("logs").mkdir(parents=True, exist_ok=True)
        log = {
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "input": validated.text,
            "raw_output": raw,
            "second_raw": raw2,
            "error": error,
            "prompt_version": "chat-v1",
        }
        with open("logs/quarantine.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(log) + "\n")

    import time as _time
    from openai import APITimeoutError, APIStatusError
    # --- first attempt with retry + timeout handling ---
    t0 = _time.perf_counter()
    try:
        completion = call_with_retry(lambda: client.chat.completions.create(model=settings.LLM_MODEL, messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": validated.text}]))
    except APITimeoutError:
        return JSONResponse(status_code=504, content={"detail": "LLM timeout after 30s"})
    except APIStatusError as e:
        if e.status_code == 401:
            return JSONResponse(status_code=500, content={"detail": "LLM auth failed (401) — check API key"})
        raise
    dur1 = int((_time.perf_counter() - t0) * 1000)
    raw = completion.choices[0].message.content or ""

    try:
        parsed = _parse_and_validate(raw)
        _log_call(settings.LLM_MODEL, getattr(completion, "usage", None), dur1, False)
        return JSONResponse(status_code=200, content=parsed.model_dump())
    except Exception as e1:
        err1 = str(e1.errors()) if isinstance(e1, ValidationError) else str(e1)
        # --- Step 3: repair once ---
        t1 = _time.perf_counter()
        try:
            repair = call_with_retry(lambda: client.chat.completions.create(model=settings.LLM_MODEL, messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": validated.text}, {"role": "assistant", "content": raw}, {"role": "user", "content": f"Your previous answer was rejected for this reason: {err1}. Return only corrected JSON matching the schema."}]))
        except APITimeoutError:
            _quarantine(raw, None, "LLM timeout after 30s on repair")
            return JSONResponse(status_code=504, content={"detail": "LLM timeout after 30s"})
        except APIStatusError as e:
            if e.status_code == 401:
                return JSONResponse(status_code=500, content={"detail": "LLM auth failed (401) — check API key"})
            raise
        dur2 = int((_time.perf_counter() - t1) * 1000)
        raw2 = repair.choices[0].message.content or ""
        try:
            parsed2 = _parse_and_validate(raw2)
            _log_call(settings.LLM_MODEL, getattr(repair, "usage", None), dur1 + dur2, True)
            return JSONResponse(status_code=200, content=parsed2.model_dump())
        except Exception as e2:
            err2 = str(e2.errors()) if isinstance(e2, ValidationError) else str(e2)
            _log_call(settings.LLM_MODEL, getattr(repair, "usage", None), dur1 + dur2, True)
            _quarantine(raw, raw2, err2)
            return JSONResponse(status_code=422, content={"detail": "Validation failed", "error": err2})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
