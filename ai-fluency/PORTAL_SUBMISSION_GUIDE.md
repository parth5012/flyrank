# FlyRank AI Fluency Internship · Master Portal Submission Guide

**Portal:** [internship.flyrank.ai](https://internship.flyrank.ai)  
**Track:** General AI Fluency · AI n-able Yourself  
**Intern:** Parth Chawla  
**Live Portfolio:** `https://portfolio-kappa-ashy-3sqgkdkyxc.vercel.app` (or your custom domain)  
**Main Evidence Repository:** `https://github.com/parth5012/flyrank`  
**Portfolio Source Repository:** `https://github.com/parth5012/portfolio`

---

## How to use this guide

Open each assignment card in the [internship portal](https://internship.flyrank.ai) and copy-paste the exact values for **Deliverable Links**, **Notes**, and **Files** from this sheet.

---

### Week 1 · What Are You Proving?
- **Deliverable links:**
  ```
  https://github.com/parth5012/flyrank/blob/main/ai-fluency/Assignment%201/week-01-what-are-you-proving.md
  ```
- **Notes:**
  > **Proof Statement:** I build reliable AI systems that work on messy, real data and stay reliable at scale because I monitor and evaluate them properly. I am proving this to a non-technical solo founder who lives in Gmail and Calendar and needs automation that doesn't break, so they will DM me on LinkedIn to pilot one with me.  
  > **Why This Needs to Exist:** My CV lists what I built, but it cannot show how it works, why I built it that way, and what tradeoffs I handled to keep it reliable at scale.
- **Files:** *(Optional: None required)*

---

### Week 1 · Draw the Path: Portfolio Sitemap + Toolkit
- **Deliverable links:**
  ```
  https://github.com/parth5012/flyrank/blob/main/ai-fluency/Week%203/through-line-content-map.md
  ```
- **Notes:**
  > Sitemap with 7 clean routes laddering to the contact action: Home (`/`), Work archive (`/projects`), Case details (`/projects/<slug>`), Reliability & failure modes (`/reliability`), Personnel file (`/about`), Build story (`/blog`), and Contact (`/contact`). Toolkit: Python, Flask, Tailwind CSS, Playwright, Vercel, Claude Projects.
- **Files:** Attach `ai-fluency/Assignment 2/sitemap.png` and `ai-fluency/Assignment 2/workspace.png`.

---

### Week 2 · Frame It as Cases: Work That Speaks for Itself
- **Deliverable links:**
  ```
  https://portfolio-kappa-ashy-3sqgkdkyxc.vercel.app/projects
  https://github.com/parth5012/portfolio/blob/main/content.py
  ```
- **Notes:**
  > Framed 5 real technical projects using the strict three-beat format: Problem, What I Built, What It Taught Me / What Broke. Hero case is Triage Desk (`/classify`) with an 8-case eval set, followed by the Task API with Supabase auth, V0-V5 Prompt Ladder, Workflow Audit, and polite Books Scraper.
- **Files:** Attach `ai-fluency/Assignment 2/response 1.png` and `response 2.png`.

---

### Week 3 · The Through-Line: Map Content & CTAs
- **Deliverable links:**
  ```
  https://github.com/parth5012/flyrank/blob/main/ai-fluency/Week%203/through-line-content-map.md
  https://portfolio-kappa-ashy-3sqgkdkyxc.vercel.app
  ```
- **Notes:**
  > Every section ladders directly up to the single primary action: "Message me about a pilot". The Hero presents the claim and real numbers (8, 60, 6); the method strip explains the 3 pillars (Evaluate, Isolate Failure, Price It); the case studies provide code and run reports; and the reliability page builds trust by naming known limitations.
- **Files:** None.

---

### Week 3 · Decide Once: Build Your Identity Kit
- **Deliverable links:**
  ```
  https://github.com/parth5012/flyrank/blob/main/ai-fluency/Week%203/identity-kit.md
  https://portfolio-kappa-ashy-3sqgkdkyxc.vercel.app
  ```
- **Notes:**
  > Palette: Deep Obsidian Navy (`#0a1628`), Surface Slate (`#111d2e`), Electric Cyan accent (`#38dafa`), Warning Amber (`#fbbf24`). Typography: Space Grotesk for headings, JetBrains Mono for metadata, telemetry, and buttons. Logo: Minimal geometric wireframe prism. Two-line style note: "Precision instrumentation over corporate gloss: deep navy backgrounds with electric cyan telemetry lines, where every piece of decorative styling mimics an active terminal or debugger."
- **Files:** None.

---

### Week 3 · Kill Your Darlings: Curate Your Images
- **Deliverable links:**
  ```
  https://github.com/parth5012/flyrank/blob/main/ai-fluency/Week%203/curate-your-images.md
  https://github.com/parth5012/portfolio/blob/main/static/og.png
  ```
- **Notes:**
  > Ruthlessly eliminated all generic AI stock art, marketing mockups, and screenshots of unrelated e-commerce UI projects (Artify Bharat). Kept exactly 4 visual elements: the 1200x630 telemetry Open Graph share card, the favicon, responsive DOM-rendered code blocks, and the FlyRank graduate badge.
- **Files:** Attach `static/og.png`.

---

### Week 4 · Three Roads: Choose Your Stack with AI
- **Deliverable links:**
  ```
  https://github.com/parth5012/flyrank/blob/main/ai-fluency/Week%204/three-roads-stack-rationale.md
  ```
- **Notes:**
  > Evaluated Carrd/Framer (no-code), Static HTML/CSS (Netlify), and Flask on Vercel. Chose Flask on Vercel because as a Python AI student, data-driven templating via `content.py` allowed me to maintain 5 cases in one file without heavy JavaScript frontend frameworks. CSS is precompiled to 35KB with no server build step.
- **Files:** None.

---

### Week 4 · Empty but Live: Ship a Blank Page
- **Deliverable links:**
  ```
  https://portfolio-kappa-ashy-3sqgkdkyxc.vercel.app
  ```
- **Notes:**
  > Deployed empty foundation over HTTPS on Vercel and confirmed reachable on mobile. Loaded initial proof statement into AI project workspace.
- **Files:** None.

---

### Week 5 · Ship the Ugly One
- **Deliverable links:**
  ```
  https://portfolio-kappa-ashy-3sqgkdkyxc.vercel.app
  https://portfolio-kappa-ashy-3sqgkdkyxc.vercel.app/projects
  ```
- **Notes:**
  > Shipped all rough routes (Home, Work, About, Contact, Story). Shared the live link with a colleague for peer feedback. Feedback noted that having a fake contact form and competing claims ("seeking internship" vs "reliable AI systems") was confusing. Planned fixes for Weeks 7-9.
- **Files:** None.

---

### Week 6 · Explain It Like You Built It
- **Deliverable links:**
  ```
  https://github.com/parth5012/flyrank/blob/main/ai-fluency/Week%206/explain-your-build.md
  https://github.com/parth5012/portfolio/blob/main/contact.py
  ```
- **Notes:**
  > Plain-words breakdown of the in-memory sliding-window rate limiter in `contact.py`. Explains how `time.monotonic()` prevents NTP clock-jump bypasses, why `collections.deque` provides O(1) eviction, and why `threading.Lock()` stops race conditions—analogous to a bouncer keeping a notebook at a movie theater door.
- **Files:** None.

---

### Week 7 · Open It on Your Phone
- **Deliverable links:**
  ```
  https://github.com/parth5012/flyrank/blob/main/ai-fluency/Week%207/phone-fix-log.md
  https://portfolio-kappa-ashy-3sqgkdkyxc.vercel.app
  ```
- **Notes:**
  > Tested all 7 routes at 390px (mobile) and 1280px (desktop) using Playwright. Shipped 7 fixes: wrapped `extra_styles` in `<style>` so raw CSS stopped rendering as visible text, solved `btn` scope collision, fixed hardcoded `inline style="flex-direction:row"` that crushed cards on phones, removed overlapping scroll cue, made submit button reusable as "SEND ANOTHER", expanded rate limit for shared IPs, and shortened wrapping text. 0 horizontal overflow and 0 console errors across all pages.
- **Files:** Attach `m-home.png` or `m-featured.png` from `/tmp/opencode/`.

---

### Week 7 · Survive the Crit (Checkpoint 1)
- **Deliverable links:**
  ```
  https://portfolio-kappa-ashy-3sqgkdkyxc.vercel.app
  https://github.com/parth5012/flyrank/blob/main/ai-fluency/Week%207/phone-fix-log.md
  ```
- **Notes:**
  > Checkpoint 1 submission. Reviewed against the design crit criteria: removed all raw CSS leakage, eliminated mobile horizontal scrolling, ensured typography scales smoothly, added visible focus indicators for keyboard navigation, and added `prefers-reduced-motion` guards.
- **Files:** None.

---

### Week 8 · Make It Do Something
- **Deliverable links:**
  ```
  https://portfolio-kappa-ashy-3sqgkdkyxc.vercel.app/contact
  https://github.com/parth5012/flyrank/blob/main/ai-fluency/Week%208/make-it-do-something.md
  https://github.com/parth5012/portfolio/blob/main/tests/test_contact.py
  ```
- **Notes:**
  > Replaced the fake `setTimeout()` contact form with a real, hardened backend endpoint (`POST /api/contact`). Features server-side string validation, hidden honeypot bot trap, sliding-window IP rate limiting, and webhook forwarding. Backed by 26 automated unit and integration tests verifying that it refuses to claim success when delivery fails.
- **Files:** None.

---

### Week 9 · Break Your Own Site (Checkpoint 2)
- **Deliverable links:**
  ```
  https://github.com/parth5012/flyrank/blob/main/ai-fluency/Week%209/where-it-breaks.md
  https://portfolio-kappa-ashy-3sqgkdkyxc.vercel.app/reliability
  ```
- **Notes:**
  > Checkpoint 2 hardening review. Attacked the site with empty inputs, garbage emails, double-submit bursts, and bot scrapers. Triaged into 10 fixed issues (including compiled Tailwind and removing CDN render-blocking scripts) and 7 transparent known limitations published openly at `/reliability`.
- **Files:** None.

---

### Week 9 · Plant Your Flag: Domain + Badge
- **Deliverable links:**
  ```
  https://portfolio-kappa-ashy-3sqgkdkyxc.vercel.app (or custom domain)
  https://github.com/parth5012/portfolio/blob/main/templates/base.html
  ```
- **Notes:**
  > Site live over HTTPS with full Open Graph and Twitter Card tags verified on OpenGraph.xyz. Favicon installed. Footer includes the FlyRank Graduate Badge with link to the verification profile.
- **Files:** None.

---

### Week 9 · The Plan to Keep Building
- **Deliverable links:**
  ```
  https://github.com/parth5012/flyrank/blob/main/ai-fluency/Week%209/keep-building-plan.md
  ```
- **Notes:**
  > Architecture designed for 30-minute updates: adding a case study requires only appending a dict to `content.py`. Named next real piece: Classifier Urgency & Confidence Calibration. Concrete reminder: recurring Sunday 6:00 PM calendar prompt and persistent Claude context.
- **Files:** None.

---

### Week 10 · Send the Link: Launch, Demo & Story (Capstone)
- **Deliverable links (one per line):**
  ```
  https://portfolio-kappa-ashy-3sqgkdkyxc.vercel.app
  https://github.com/parth5012/flyrank/blob/main/ai-fluency/Week%2010/demo-script.md
  https://github.com/parth5012/flyrank/blob/main/ai-fluency/Week%2010/build-write-up.md
  https://github.com/parth5012/flyrank/blob/main/ai-fluency/Week%2010/build-story.md
  [PASTE YOUR 4-MINUTE LOOM / UNLISTED YOUTUBE VIDEO LINK HERE]
  ```
- **Notes:**
  > **Capstone Submission:**
  > 1. **Live Portfolio:** Launched on Vercel over HTTPS, proving one claim ("I build AI systems that keep working on messy real data because I measure them instead of guessing"), filled with 5 real cases.
  > 2. **One Real Feature Working:** End-to-end verified contact form with server-side validation, honeypot, rate limiting, and 26 pytest tests.
  > 3. **The 4-Minute Demo:** Follows `demo-script.md`: walks the live site, shows the triage classifier and eval sets, executes 3 live form submissions (empty, garbage, valid), demonstrates delivery, reviews the `/reliability` page, and shows the 26 automated tests.
  > 4. **Build Write-Up:** Documents the Flask stack decision, the hardest break (the contact form that initially lied), what we'll build next (urgency scoring), and an honest breakdown of where AI assisted vs human decisions.
  > 5. **Build-in-Public Story:** Published on the site at `/blog` and on social.
- **Files:** Attach the exported demo video MP4 if under portal upload limits.
