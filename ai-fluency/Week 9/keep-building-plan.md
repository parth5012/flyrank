# Week 9 · The Plan to Keep Building

**Assignment:** Exactly where your next case study goes, the 30-minute steps to add one reusing the Week 2 three-beat shape, the named next piece of real work, and a concrete reminder to do it.

---

## 1. Where the next case study goes

The architecture of this portfolio was refactored specifically so adding a new case study never requires editing HTML templates, updating navbars, or touching routing code.

All project data lives in a single Python data structure:
**`content.py`** in the `portfolio` repository root, within the `CASES` list.

Adding a case is simply appending a dictionary to `CASES`:
```python
{
    "slug": "classifier-urgency-eval",
    "title": "Triage Desk: Calibrated Urgency",
    "tagline": "Scoring priority alongside category so urgent bugs never wait",
    "summary": "Extending the 8-case eval set to score urgency (low/normal/high) with confidence calibration...",
    "problem": "...",
    "built": "...",
    "learned": "...",
    "facts": [("Eval cases", "16"), ("Urgency score", "90%+"), ("Latency p95", "1.1s")],
    "stack": ["Python", "FastAPI", "OpenRouter", "Pydantic"],
    "source_url": "https://github.com/parth5012/flyrank/tree/main/backend/Assignment%206",
    "source_label": "Source & calibrated eval harness",
}
```

Once appended and committed:
- The **Work archive (`/projects`)** renders the new card automatically.
- The **Dynamic detail route (`/projects/<slug>`)** generates the dedicated three-beat page with breadcrumbs and related case recommendations.
- Global navigation, sitemap, and internal links stay valid without template edits.

---

## 2. The 30-Minute Addition Checklist

Whenever a feature, bugfix, or evaluation run ships:

1. **Extract the 3 beats (10 minutes):**
   - **The Problem:** What was dirty or broken before? (Never describe what the code does; describe the failure mode or operational pain).
   - **What I Built:** Architecture, constraints, schemas, retry/isolation policies, exact commands.
   - **What It Taught Me / What Broke:** The honest measurement. One metric, one surprise, and one remaining limitation.
2. **Add entry to `content.py` (5 minutes):**
   - Fill the dictionary fields: `slug`, `title`, `tagline`, `summary`, `problem`, `built`, `learned`, `facts`, `stack`, `source_url`.
3. **If new CSS utility classes were used, rebuild CSS (2 minutes):**
   - Run `npm run build:css` (compiles to `static/tailwind.css`).
4. **Run the local verification suite (3 minutes):**
   - `.venv/bin/python -m pytest tests/ -q`
   - Test new route locally: `curl -I http://127.0.0.1:5000/projects/<new-slug>`
5. **Update `/reliability` if a known limitation was solved (5 minutes):**
   - Move resolved limitation from `BREAKS` to completed or adjust the notes.
6. **Commit & Deploy (5 minutes):**
   - `git add content.py static/tailwind.css && git commit -m "feat(portfolio): add <name> case study"`
   - `git push origin main` (triggers automatic Vercel production deployment).

---

## 3. The Named Next Piece of Real Work

**Project:** Classifier Urgency & Confidence Calibration (`backend/Assignment 6`)
**What will be built:**
1. Record real-model evaluation scores for the existing 8 cases using `openai/gpt-4o-mini` (replacing the 2/8 stub baseline).
2. Expand the eval harness (`evals/cases.json` and `evals/run.py`) to score `urgency` (`low`, `normal`, `high`) in addition to `category`.
3. Add a confidence threshold test: if confidence is below 0.6, force classification to `other` to protect downstream triage teams from hallucinatory certainty.

---

## 4. The Concrete Reminder

- **Calendar Event:** Recurring weekly calendar event on Google Calendar every Sunday at 6:00 PM IST: *"Ship or Update One Case Study on parthchawla portfolio"*.
- **Repository Hook:** A GitHub issue template in `parth5012/flyrank` titled `Case Study Candidate` triggered when an assignment/feature branch merges.
- **AI Workspace Continuity:** The Claude Project / cursor rules retain `context-doc.md`, this `keep-building-plan.md`, and `content.py` so prompts immediately match the established 3-beat voice and JSON format.
