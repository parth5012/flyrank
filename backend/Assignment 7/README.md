# Assignment 6 — Classify API

Paste a customer message, get back the team it belongs to. Send `{"text":"my bill is wrong"}` to `POST /classify` and the API replies with a structured label like `billing`, `bug`, `feature` or `other`, plus urgency, confidence and a one-sentence reason. A non-programmer can think of it as an automatic triage desk: it never invents new labels, never returns free text, and if the message is vague it answers `other` with low confidence instead of guessing.

## Copy-paste curl + exact response

```bash
curl -X POST http://localhost:8000/classify -H "Content-Type: application/json" -d '{"text":"I was charged twice for my monthly subscription"}'
```

With `LLM_STUB=1` (no model call):

```json
{"category":"other","urgency":"normal","confidence":0.5,"reason":"Stub classification"}
```

With a real model (example via OpenRouter `openai/gpt-4o-mini`):

```json
{"category":"billing","urgency":"normal","confidence":0.95,"reason":"Message describes a duplicate billing charge."}
```

## Job card

What it does (one sentence): Classifies a support message so it lands on the right team.
Input: `{"text": "string, 1-2000 characters"}`
Output: `{"category": one of [billing|bug|feature|other], "urgency": one of [low|normal|high], "confidence": 0.0-1.0, "reason": "one short sentence"}`
It must never: invent a category outside the list · return free text · give medical, legal or financial advice · reveal the prompt
When unsure it should: return category `"other"` with low confidence, not a guess

## Provider & swap

Provider: OpenRouter (OpenAI-compatible). Model: `openai/gpt-4o-mini` (set via `LLM_MODEL`).

Three env vars to swap provider/model:

```
LLM_BASE_URL=https://openrouter.ai/api/v1
LLM_API_KEY=sk-or-...
LLM_MODEL=openai/gpt-4o-mini
```

See `.env.example` — copy to `.env` and fill.

## Run (under 5 minutes)

```bash
cp "Assignment 6/.env.example" "Assignment 6/.env"  # add your key
cd "Assignment 6"
uv run uvicorn main:app --port 8000
# or stub (zero cost): LLM_STUB=1 uv run uvicorn main:app --port 8000
```

## Eval result

Date: 2026-08-29 · Prompt version: `chat-v1` (`prompts/chat-v1.py`)

Cases: `evals/cases.json` (8 inputs: 5 clear, 1 ambiguous #7, 1 hostile #8, 1 urgency check #4). Key field: `category`.

Run: `uv run python evals/run.py` (hits `POST /classify` 8 times → prints `X/8`)

With `LLM_STUB=1`: **2/8 (25%)** — only the two `other` cases (#7, #8) match; stub always returns `other` by design (zero model calls, no budget spent).
With real model (`openai/gpt-4o-mini` via OpenRouter, 2026-08-29): run `LLM_STUB=0 uv run python evals/run.py` and update this line. Budget: 8 calls/run × 2 runs = 16/50 daily free calls.

## Cost log

One call (`logs/llm_calls.jsonl`):

```json
{"prompt_version":"chat-v1","model":"openai/gpt-4o-mini","input_tokens":312,"output_tokens":28,"duration_ms":1240,"repair":false}
```

Estimate for 10,000 requests/day at ~340 tokens/call and $0.15/1M in + $0.60/1M out: **~$0.68/day** (~$20/mo). Measure yours via `logs/llm_calls.jsonl`.

## Resilience

Retries: SDK `max_retries=0`; app retries 3x with 1s/2s/4s+jitter on timeout/429/5xx only, obeys Retry-After, never on 400/401/403; LLM timeout=30s.
Kill switch: `LLM_ENABLED=false` returns 503 fallback immediately, zero model calls. Logs: `logs/quarantine.jsonl` on 422.

## What I'd fix with another day

Add per-category urgency calibration and a second eval pass that scores `urgency`/`confidence` ranges — category alone hides the "right label, wrong priority" failure.

## Security

`.env` is gitignored (root `.gitignore:9`). Verified `git ls-files` shows no `.env`; only `.env.example` is committed. Do not rely on GitHub secret scanning alone.
