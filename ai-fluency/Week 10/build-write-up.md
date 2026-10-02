# Build write-up — what I chose, what broke, what's next

*Companion to the demo. This is the document a reviewer reads after watching.*

---

## 1. The stack decision

**What I used:** Flask + Jinja templates, Tailwind CSS compiled to one static file, deployed as
a Python serverless app on Vercel. One custom domain over HTTPS.

**The three roads I weighed:**

| Road | What it is | Why I did not pick it | Why it was still a real option |
|---|---|---|---|
| **No-code builder** (Carrd, Framer) | Drag-and-drop site | It would have looked finished in a day and proved nothing. My evidence is code, run reports and terminal output — not images. I would still have had to write the case studies by hand. | Fastest route to a live URL. Genuinely right if the work were visual. |
| **Framework** (React, Next) | Full developer setup | Weeks of build tooling before a stranger sees a page. The program explicitly warns this is where people stall. My site is seven pages and one form; the tooling would have cost more than the content. | The right call if the site became something with real state. |
| **Plain code with a Python framework** ← **chosen** | Hand-written HTML/Jinja on Vercel | Fastest, free, and I can explain every line, which Week 6 required and a framework would have made harder. | It already worked — my existing site was Flask — so switching meant rewriting for no gain. |

**The real trade-off I accepted:** Jinja means no component reuse. Adding a page means copying
markup. I mitigated it by putting every case in one Python dict (`content.py`), so the index,
the detail pages and the links are all generated — a new case is a dict, not a template rewrite.
If the site grows past about fifteen cases, that stops working and I would move to a static site
generator. That's the point at which I'd switch, and I know where it is.

**Why Flask and not plain HTML?** Honestly: inertia. The site already existed in Flask and it
works. The honest version is that I chose the path of least resistance, not the path of least
complexity. If I'd started today with this exact content I'd have written static HTML and served
it with no server at all, and the only dynamic piece would have been a form handler.

**Can I maintain this?** Yes. One file holds all the content. One command rebuilds the CSS. One
command runs 26 tests. Nothing needs a database.

---

## 2. The hardest thing that broke

**The contact form lied to me.**

The original form's submit handler was this:

```js
// Simulate async send (replace with real fetch to backend endpoint)
setTimeout(() => {
  btn.classList.add('hidden');
  success.classList.remove('hidden');
  document.getElementById('contact-form').reset();
}, 1000);
```

No request. No server. No storage. It displayed "Message sent!" and discarded the message. Every
visitor would have been told their message was delivered when it was thrown away.

**Why it matters more than a crash.** A crash is loud. This was quiet, it looked finished, and
it was in the one place on the site where a visitor is trying to reach me. It was only found
because Week 9 told me to attack my own site, and I submitted a message and then checked whether
anything arrived.

**What I built instead.** A real endpoint with server-side validation (name, email shape, message
length), a honeypot field that answers bots identically to humans while delivering nothing, a
per-IP rate limit, and a POST to a webhook. The rule I set for myself: **it cannot report a
success it did not achieve.** If the webhook is unset, unreachable, or returns an error, the
endpoint returns a real error and the page shows it. There is a test for exactly this:

```python
def test_it_never_claims_success_when_no_webhook_is_configured(...):
    ... assert response.status_code == 503
```

**The second break, found by testing in a browser:** after one successful send, the submit
button was hidden permanently, so the form was unusable without a page reload. The server was
fine; the UI was broken. Unit tests did not catch it — it took driving the real form in a real
browser and submitting twice on the same page view. That's the argument for the browser test
being part of the deliverable and not an extra.

---

## 3. What I'd build next

**Extend the classifier eval to score urgency, not just category.** Right now the contract
returns `low / normal / high` urgency and the eval set only checks the category. So a response
that picks the *right team with the wrong priority* passes silently — which for a triage desk is
a real failure, because the team gets it at the wrong time. The fix is a second eval pass
scoring urgency, plus calibration per category. It's named on `/reliability` as a known
limitation, and it's the next case that goes up on this site.

Concretely, next: add urgency expectations to the 8 cases, score them separately, record both
numbers, and write up whether the model is confidently wrong.

---

## 4. The honest caveat

This portfolio was built with heavy AI assistance, and I think that's the correct trade for the
speed. But I want to be precise about what that means, because the easy version of this story
is a brag and the accurate version is more interesting:

AI wrote nearly all the code. What it did **not** do was decide what the site should claim,
notice that my three original projects couldn't support that claim, build the eval set, choose to
publish the failure list, or work out that a fake success message is unacceptable. Those were the
decisions, and they were the work.

The clearest evidence is the contact form. An AI produced a plausible-looking handler that threw
messages away. Nothing flagged it until I tried to break my own site. **A plausible demo path is
exactly what AI will cheerfully build for you**, and the only defence I found is attacking your
own work before someone else does.