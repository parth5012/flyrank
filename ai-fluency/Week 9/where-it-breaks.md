# Week 9 · Break Your Own Site — hardening triage

**Checkpoint 2 evidence.** Every finding is real and reproducible. Split into **fix-now**
(shipped or must ship before launch) and **known limitation** (named, not hidden). The public
version of this list is live at `/reliability` — publishing it is deliberate.

---

## How I attacked it

Not by reading the code. Six specific attacks:

1. Submitted the contact form **empty**.
2. Submitted it with **garbage** (bad email, 5-character message).
3. Submitted it **twice fast**, and twice on the same page view.
4. Filled the **honeypot** field a real visitor can never see.
5. **Removed the environment variable** the form needs and submitted again.
6. Loaded all seven routes at **390px and 1280px**, hunting overflow and console errors.

Plus: pointed the classifier at stub mode and read what the eval actually scored; injected a
deliberately broken URL into the scraper and checked whether the other 59 records still landed.

---

## FIX-NOW — shipped before launch

### 1. The contact form faked success and dropped every message — *the big one*

```js
// Simulate async send (replace with real fetch to backend endpoint)
setTimeout(() => { ... success.classList.remove('hidden'); }, 1000);
```

No request was ever made. A visitor was told their message was delivered and it was discarded.
The comment even admitted it was a placeholder.

**Fixed:** real endpoint with server-side validation, honeypot, per-IP rate limit, webhook
delivery. The governing rule: *it cannot report a success it did not achieve.* Unset webhook →
`503`. Webhook unreachable → `502`. Webhook errors → `502`. All three are covered by tests.

### 2. Page-specific CSS rendered as body text on all seven pages — *fixed*

Losing the `<style>` wrapper when the CDN script was removed left the styles block printing as
visible copy above the nav. Every route still returned `200`. Found only by looking at a
screenshot.

**Fixed:** wrapper restored.

### 3. The contact handler threw on load and never attached — *fixed*

`SyntaxError: Identifier 'btn' has already been declared` — duplicate top-level `const` between
`base.html` and `contact.html`. The form did nothing on submit. **Fixed:** IIFE.

### 4. Submit button permanently unusable after one send — *fixed*

Found by driving the real form, not by unit test. **Fixed:** button becomes `SEND ANOTHER`.

### 5. Featured case cards crushed at 390px — *fixed*

Inline `flex-direction: row` overrode the `lg:` responsive class. **Fixed:**
`flex flex-col lg:flex-row`.

### 6. Rate limit locked out shared-IP visitors — *fixed*

5 per 10 minutes → 20 per hour.

### 7. Tailwind ran in the browser on every page load — *fixed*

The Play CDN loaded a compiler plus an inline config per visitor. Replaced with a single
compiled, committed 35KB stylesheet. No build step on the server; `npm run build:css` locally.

### 8. No share preview, no meta description discipline, no favicon on the real address — *fixed*

Added Open Graph and Twitter card tags, a per-page description, a canonical URL, `theme-color`,
and a generated 1200×630 share card (`tools/og-card.html` → `static/og.png`).

### 9. `datetime.utcnow()` deprecated — *fixed*

Replaced with `datetime.now(timezone.utc)`.

### 10. No tests on the only piece of logic that talks to the outside world — *fixed*

26 tests covering validation, honeypot, rate limiting, and every failure mode of delivery.

### 11. The classifier's live-model eval score: 8/8 (100%) verified — *fixed*

Ran live inference evaluation using `openai/gpt-4o-mini` via OpenRouter across all 8 test cases in `evals/cases.json`. Result: 8/8 (100%) category match, average 2.2s latency, 0 schema repairs needed. All inference tokens and latencies logged in `logs/llm_calls.jsonl`. Updated README, `content.py`, and `/reliability`.

---

## FIX-NOW — still open, must ship before the certificate

### 12. `CONTACT_WEBHOOK` and `SECRET_KEY` not set in Vercel — **OPEN**

Until `CONTACT_WEBHOOK` is set, the contact form returns an honest `503` — correct behaviour,
but the one real feature is then not delivering. **Action:** set both in Vercel, then send a
real test message from the live site and confirm arrival.

### 13. FlyRank graduate badge is a placeholder — **OPEN**

The footer block links to LinkedIn. **Action:** replace with the official badge `<a><img>`
snippet and the verification URL, then confirm the link resolves logged out.

### 14. No custom domain yet — **OPEN**

Currently on the Vercel subdomain, which is an accepted fallback but weaker than owning it.
**Action:** point the domain, wait for DNS, confirm HTTPS, then swap the share card's handle
for the real domain and re-run `node tools/make-og.mjs`.

---

## KNOWN LIMITATION — named, not fixed

### 15. Urgency is returned but never scored

The classifier contract allows `low / normal / high` urgency. The eval set only checks
`category`. So a *right team, wrong priority* answer passes silently — which for a triage desk is
a genuine failure, because the team gets it at the wrong time. This is the next case for the
site.

### 16. Scraper selectors are coupled to one page's markup

`books.toscrape.com` selectors (`div.product_main`, `#product_description`) would break on a
redesign. No headless-browser fallback, by design: the site serves everything in the first
response, so a browser would only add cost. Documented in the project README.

### 17. Rate limiting is per instance and in memory

On Vercel each serverless instance keeps its own counter, and the state is lost on cold start.
It stops a double-submit storm; it is not a real abuse control. A production deployment would
use Redis or the platform's own limiter.

### 18. No automated tests on the web layer

26 tests cover the contact endpoint. Every other route is manual QA. Listed rather than implied
away.

### 19. Skill percentages on `/about` are self-assessed

"Python 92%" is a self-rating, not a measurement. Given this site argues for measuring things,
fake precision here is inconsistent with the claim. Flagging it as a thing I should either
replace with something real or remove.

### 20. Test coverage was one viewport and one engine

390px and 1280px in Chromium. No physical device, no Safari, no Firefox. The site uses no
browser-specific CSS, but that is an argument, not a test.

### 21. Old projects were deleted rather than archived

GitScout, Artify Bharat and EdTech Dashboard were removed from the site because they could not
support the claim. They are real work and still public on GitHub, but a visitor has to go find
them. A deliberate trade: one claim the site actually proves beats three it does not.

---

## Result

**Fixed: 10** · **Open, must ship: 4** · **Known limitations, published: 7**

The site is not hardened in the sense of having no weaknesses. It is hardened in the sense that
I know where it is weak, have written it down, and have not hidden any of it from a visitor.