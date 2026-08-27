# Assignment 6 — Classify API

`POST /classify` (alias `/chat`) — Input `{text}` → Output `{category, urgency, confidence, reason}` per JOB-CARD.md. Validation via Pydantic, stub mode for zero-cost dev.

## Run

```bash
cd "Assignment 6"
LLM_STUB=1 uv run uvicorn main:app --port 8000
```

## Test (5 sec) — with LLM_STUB=1, zero model calls

Valid (200, matches schema):
```bash
curl -X POST http://localhost:8000/classify -H "Content-Type: application/json" -d '{"text":"my bill is wrong, I was charged twice"}'
# -> {"category":"billing","urgency":"normal","confidence":0.5,"reason":"Stub classification"}
```

Broken — missing field (400 naming field):
```bash
curl -X POST http://localhost:8000/classify -H "Content-Type: application/json" -d '{}'
# -> 400 {"field":"text","detail":[...]}

curl -X POST http://localhost:8000/classify -H "Content-Type: application/json" -d '{"text":""}'
# -> 400 field text (too short)

curl -X POST http://localhost:8000/classify -H "Content-Type: application/json" -d '{"text":"'"$(python -c 'print("x"*2001)')"'"}'
# -> 400 field text (too long, max 2000)
```

Wrong type (400):
```bash
curl -X POST http://localhost:8000/classify -H "Content-Type: application/json" -d '{"text":123}'
# -> 400 {"field":"text"}
```

Schema: `src/llm/schema.py` — `category`/`urgency` enums, `confidence 0-1`, `reason` max 256, `text` 1-2000 chars. Output file `llm/schema.py` is the source of truth.
Stub: `LLM_STUB=1` skips model and returns hard-coded valid object. No OpenRouter call.
