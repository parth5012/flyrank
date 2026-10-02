# Demo script — 4 minutes, recorded, no re-takes

**Rule for the whole recording: every link you open must already be live.** Open the live
site in a private window logged out before you press record.

Total: 4:00. Leave 20 seconds of slack.

---

## 0:00 — Cold open (0:20)

Browser already on the live URL. No intro music, no "hi I'm Parth" title card.

> "This is my portfolio. One sentence says what I do: I build AI systems that keep working on
> messy real data, because I measure them instead of guessing. In four minutes I'll show you
> the work, one feature that genuinely works, and the list of everything that's still broken."

**Do not** say "AI engineer" or "seeking an internship". That is the old version of this site.

---

## 0:20 — The claim and the method (0:30)

Stay on the home page. Scroll slowly to the three method blocks.

> "Three things show up in every case. Evaluate: a written set of test cases, including the
> ambiguous and hostile ones. Isolate failure: bad output gets quarantined instead of passed
> downstream. And price it: every call logs tokens, latency and retries."

Point at the three numbers — 8 eval cases, 60 records validated, 6 prompt versions. Every one
is from a real run.

---

## 0:50 — The featured case (0:50)

Click **Read the case** on Triage Desk.

> "This is a support-message classifier. It returns one of four teams, an urgency and a
> confidence score, and it's not allowed to invent a fifth label. The interesting part is that
> it returns `other` with low confidence when the message is vague, instead of guessing."

Scroll through the three beats. Land on **what it taught me**:

> "The stub mode scored 2 out of 8, and that was the useful result — it proved the harness
> measures the prompt, not the plumbing, because the plumbing was identical in both runs."

Then point at the amber **where it still breaks** block. Do not skip it.

---

## 1:40 — The one feature, working live (0:50)

Go to **/contact**. Show the empty form.

> "This form used to lie. It said 'Message sent' and dropped every message on the floor —
> there was no server call at all, just a timer. I found it by trying to break my own site."

Now do three real submissions, in this order:

1. **Empty submit** → screenshot the three errors: *name is required, email is required,
   message is required.*
2. **Garbage submit** (`not-an-email`, `short`) → *that email address does not look right,
   please write at least 10 characters.*
3. **Real message** → green *Message sent. I will reply from…*, and the button becomes
   **SEND ANOTHER**.

Then open the inbox where the webhook delivers and show the message arrived, with the name
and email filled in.

> "If the webhook is unset or fails, it returns an honest error instead of a green tick.
> There's 26 tests behind this endpoint."

---

## 2:30 — Where it breaks (0:40)

Go to **/reliability**. Scroll the whole list.

> "Two of these are fix-now and four are known limitations. The known ones I chose not to fix:
> urgency is returned but never scored, the scraper selectors are coupled to one page's markup,
> rate limiting is in-memory, and there's no automated test coverage on the rest of the web
> layer."

Say this line: **"I'd rather you find these than have me claim there weren't any."**

---

## 3:10 — AI did the heavy lifting (0:30)

Switch to the terminal.

> "One honest note on AI. It wrote essentially all the code here — the templates, the contact
> endpoint, the validation, the tests. What it bought me was time to spend on the parts that
> are actually mine: the eval set, deciding what to leave out, and choosing to publish this
> list instead of hiding it."

Then show one concrete artefact:

```bash
.venv/bin/python -m pytest tests/ -q
```

> "26 tests. The one that matters most asserts the endpoint never claims success when no webhook
> is configured."

---

## 3:40 — The ask and the end (0:20)

Back to the home page.

> "If you have automation that has to survive real data, send me the messy case and I'll tell
> you what I'd measure first. Link's in the footer."

Stop. **4:00.**

---

## Before you record — checklist

- [ ] Site merged to `main` and deployed to Vercel on the real URL
- [ ] `CONTACT_WEBHOOK` and `SECRET_KEY` set in Vercel env vars
- [ ] **Send yourself a test message from the live site and confirm it arrived**
- [ ] Badge installed in the footer with the real verification link
- [ ] Custom domain resolving over HTTPS, opened once on your phone
- [ ] Live URL tested logged out in a private window
- [ ] Share preview checked at opengraph.xyz
- [ ] Classifier's live eval score recorded in the README (see below)

## One thing to do before you record

The classifier README still says *"run `LLM_STUB=0 uv run python evals/run.py` and update this
line"* — the real-model score was never recorded. Run it once with your key and paste the number
in. It takes about 30 seconds, it fills the one remaining fix-now item on `/reliability`, and it
gives you a real number to say out loud instead of "I didn't get to it".

If you run it live on camera instead, that's an even better demo beat — but then update the
README with the number afterwards, because the site currently says it's missing.