# FL-01 — AI Workflow Audit and Tool Setup

**Intern:** Parth Chawla
**Track:** General AI Fluency
**Date:** 2026-08-30
**Status:** Audit complete. Tool evidence verified — Claude account + Project (screenshot `evidence/claude-parth-project-setup.png`), ChatGPT account, Anthropic Academy `AI Fluency: Framework & Foundations` certificate (`ai fluency.pdf`).

## Purpose and boundary

This audit maps recurring work from my FlyRank internship, B.Tech CSE (AI & DS) study, Obsidian second-brain build, and side project `vela` (personalized assistant). It is not a claim that every future workflow is automated. I use AI to draft, check, and iterate. I remain responsible for learning, safe data handling, evidence review, and every final submission.

My current stack: Python, RAG pipelines (pgvector / ChromaDB), LangGraph / LangChain orchestration, FastAPI / Django + Celery, vector DBs and embeddings, Gemini / OpenAI / Claude / Llama / Mistral. Proof statement for this track: *I build reliable AI systems that work on messy, real data and stay reliable at scale because I monitor and evaluate them properly* — for a non-technical solo founder who lives in Gmail and Calendar, so they DM me on LinkedIn to pilot one.

## Recurring workflow audit

14 tasks. Classification is one of: `Just me` / `Delegate to AI with review` / `Collaborate with AI` / `Fully automate`.

| # | Recurring task | Classification | One-line rationale |
|---|---|---|---|
| 1 | Plan weekly FlyRank assignments and AI OS work from `priorities.md` / TickTick | Collaborate with AI | AI turns requirements into a checklist; I set priorities and commitments |
| 2 | Convert a FlyRank assignment card into a deliverable outline | Collaborate with AI | AI extracts requirements; I verify against the actual card |
| 3 | Build and debug `vela` features — RAG, multi-agent, tool calling | Collaborate with AI | AI suggests architecture/fix; I run code and inspect results |
| 4 | Run FastAPI/Django endpoints and diagnose failures | Collaborate with AI | AI helps read tracebacks; I execute and validate the fix |
| 5 | Interpret evaluation / validation results and approve claims | Just me | I must decide what the evidence actually supports |
| 6 | Review material for privacy before pasting into any AI tool | Just me | I keep raw data, secrets, and identifying material out of public artifacts |
| 7 | Debug an exact Python, Git, or Markdown error | Delegate to AI with review | AI proposes narrowest fix; I test before keeping it |
| 8 | Draft a public-safe capstone / README explanation | Collaborate with AI | AI improves clarity; I fact-check every technical statement |
| 9 | Choose a chart or visual for a case study | Collaborate with AI | AI critiques reader fit; I verify metric and scope |
| 10 | Update README headings, docs, and `connections.md` | Delegate to AI with review | AI drafts consistent wording; I check links and facts |
| 11 | Check repo status and guard against tracked datasets/secrets | Fully automate | Repeatable, low-risk, objective check |
| 12 | Write an employer-facing project summary (LinkedIn / portfolio) | Collaborate with AI | AI tailors language; I ensure tools and results are truthful |
| 13 | Complete Anthropic Academy learning and certification assessment | Just me | Learning and assessment must be my own understanding |
| 14 | Rehearse a 5-minute explanation of my build | Just me | AI can quiz me, but I must explain my own tradeoffs |

Coverage: 4× Just me, 2× Delegate with review, 7× Collaborate, 1× Fully automate — satisfies the "at least two Just me" rule.

## Three target tasks for FL-02 through FL-04

These are the reusable tasks this audit defines for the next assignments. Each has a measurable "done well means" bar.

| Target task | Done well means |
|---|---|
| **Turn technical evidence into a public-safe case-study section** | 275–350 words; states problem, validation approach, observed result, recommendation; every concrete claim traces to supplied evidence; no causal or client-specific claim |
| **Write an employer-facing summary of one completed project (e.g. `vela` or scraper)** | Exactly 3 sentences, 90–120 words; names real tools/methods, states one verified result, no private data or inflated language |
| **Create and critique a portfolio sitemap for an early-career AI profile** | ≤5 primary nav items, visible case-study path, one clear contact/action route, one purpose + CTA per page; never claims an unshipped page is live |

## Claude Project setup — custom instructions (verbatim, as saved)

> I am Parth Chawla, 3rd-year B.Tech CSE (AI & DS) building `vela` (personalized assistant) and an Obsidian second brain. Stack: Python, RAG (pgvector/ChromaDB), LangGraph/LangChain, FastAPI/Django + Celery, vector DBs, Gemini/OpenAI/Claude/Llama/Mistral. Goals: ship the AI OS, scale Obsidian, finish Hands-On Machine Learning (O'Reilly), maximize FlyRank AI Internship, and prepare for freelancing for solo founders who live in Gmail/Calendar.
>
> Use a practical, concise, supportive tone and plain English. Short sentences. Bullets over paragraphs. Work on one clearly defined task at a time. Before proposing repo changes, inspect the relevant requirements and files. Never invent results, tools, links, employers, credentials, or data. Treat raw datasets, client identifiers, secrets, and personal information as private — do not ask me to paste them and do not suggest committing them. Clearly label assumptions and drafts. Tie technical claims to provided evidence and recommend a simple verification step. For debugging, use the exact error output and propose the smallest testable fix first.

Project name in Claude: `Parth — AI Fluency / vela` (or similar). Screenshot: `evidence/claude-parth-project-setup.png` — shows Project title and Instructions panel expanded. Redacted for public safety (no tokens, passwords, private prompts, unrelated tabs, or notifications visible).

## Evidence record and completion gate

| Required evidence | Status | Location / note |
|---|---|---|
| Claude account available | Complete | Screenshot `evidence/claude-parth-project-setup.png` shows logged-in Project |
| Claude Project with custom instructions saved | Complete | Same screenshot — Instructions panel visible |
| ChatGPT account available | Complete | Verified account; redacted screenshot available on request (not committed with tokens) |
| Anthropic Academy enrollment — AI Fluency: Framework & Foundations | Complete | Certificate `ai fluency.pdf` (Parth Chawla) — attached to FlyRank submission, not exposing credential ID publicly |
| First Academy module completed | Complete | Same certificate proves full course completion, which exceeds the first-module requirement |

**Submission gate — screenshot safety check before uploading to FlyRank:** no passwords, access tokens, raw data, client-identifying material, private prompts, unrelated browser tabs, desktop notifications, or unnecessary personal identifiers visible. Certificate file is attached directly to the FlyRank card; only the redacted Project screenshot is committed to the public repo.

## References

[1] Ethan Mollick, "On-boarding your AI Intern" — https://www.oneusefulthing.org/p/on-boarding-your-ai-intern
[2] Anthropic Academy, "AI Fluency: Framework & Foundations" — https://anthropic.skilljar.com/ai-fluency-framework-foundations
[3] Claude Help Center, "What are projects?" — https://support.claude.com/en/articles/9517075-what-are-projects
