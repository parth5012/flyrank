# Week 4 · Three Roads: Choose Your Stack with AI

**Date:** 2026-09-14  
**Track:** AI Fluency · AI n-able Yourself

---

## 1. Input Constraints

- **Budget:** $0.00 (Strictly free tools and hosting tiers only).
- **Skill Level:** 3rd-year B.Tech CSE (AI & Data Science). Confident in Python, backend APIs, data pipelines, and CLI tooling. Moderate familiarity with HTML/CSS. Not interested in deep frontend framework ecosystem complexity (Webpack/Vite/Next.js hydration debugging).
- **What It Needs to Do:** Host 5 case studies with 3-beat breakdowns, show live telemetry/metrics, provide a `/reliability` transparency page, and support one working contact form with server-side validation.
- **How Work Must Be Displayed:** Monospace code blocks, terminal outputs, curl examples, schema definitions, and clean readable long-form text.
- **Dynamic Requirement:** Exactly one dynamic feature: a working contact form that validates inputs, drops spam, rate-limits abuse, and forwards messages to my inbox.

---

## 2. The Three Roads Evaluated

| Road | Option 1: No-Code (Carrd / Framer) | Option 2: Plain HTML/CSS on Netlify | Option 3: Python Web Service (Flask on Vercel) ← **CHOSEN** |
|---|---|---|---|
| **How to Build** | Visual drag-and-drop editor. | Hand-written HTML/CSS + Tailwind CLI. | Python Flask application with Jinja2 templating and precompiled Tailwind CSS. |
| **Hosting** | Free tier on Carrd or Framer subdomain. | Free static tier on Netlify or Cloudflare Pages. | Free Serverless Function tier on Vercel (`vercel.com`). |
| **Backend Required?** | No (uses third-party form handler). | No (uses Netlify Forms or Formspree). | Minimal embedded backend (Flask blueprint handling `/api/contact` and routing). |
| **How Work is Shown** | Visual blocks; code snippets look awkward and formatted like marketing copy. | Excellent; clean readable prose and styled `<pre><code>` blocks. | Outstanding; native Python data structures (`content.py`) feed templated cases. |
| **The Real Trade-off** | You don't own the code, cannot automate case generation, and export is locked. | Every new case requires manual HTML duplication unless a static site generator is introduced. | Serverless cold starts (~400ms); slightly higher deployment configuration than pure static HTML. |

---

## 3. Pressure-Testing the Front-Runner (Flask on Vercel)

- **What breaks if I pick the simplest (Carrd)?** I would have had a live page in three hours, but it would look like a product landing page rather than an engineer's portfolio. I couldn't write custom server-side validation tests or showcase Python craft.
- **What do I have to maintain if I pick the most powerful (Next.js / React)?** React state management, hydration errors, npm dependency updates, build tooling, and thousands of lines of boilerplate for a website that is fundamentally a reading experience.
- **Can I finish in time?** Yes, because an existing Flask foundation already worked. Rebuilding it with structured data in `content.py` took under a day.
- **Can I maintain this?** Completely. Adding a case study requires only modifying a Python dictionary in `content.py`. The CSS is precompiled to 35KB, requiring zero Node.js build commands during production deployment.

---

## 4. The Rationale & Empty-but-Live Verification

### Why Option 3 (Flask on Vercel) was chosen:
1. **Leverages Core Strength:** As an AI/backend student, Python is second nature. Writing route handlers and Pydantic/Python validators is intuitive and testable with standard `pytest`.
2. **Data-Driven Architecture:** Having `content.py` drive both `/projects` and `/projects/<slug>` prevents copy-paste errors across HTML files while avoiding complex JavaScript build frameworks.
3. **True Ownership:** The entire codebase is transparent, open-source, version-controlled in Git, and runs locally with one command:
   ```bash
   python -m flask --app app run --port 5000
   ```

### "Empty but Live" Milestone
- **Live URL:** `https://portfolio-kappa-ashy-3sqgkdkyxc.vercel.app`
- **Confirmed on Mobile:** Opened and verified on iPhone 14 / mobile browser over HTTPS.
