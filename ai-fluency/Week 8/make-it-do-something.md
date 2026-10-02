# Week 8 · Make It Do Something: Real Working Contact Pipeline

**Date:** 2026-10-02  
**Track:** AI Fluency · AI n-able Yourself

---

## 1. The One Dynamic Feature

**A server-validated, spam-protected, rate-limited Contact Form (`/contact` → `POST /api/contact`).**

Before this week, the site had a cosmetic form that faked submission using JavaScript `setTimeout()`:
```javascript
// The fake version that had to be destroyed:
setTimeout(() => {
  btn.classList.add('hidden');
  success.classList.remove('hidden');
  document.getElementById('contact-form').reset();
}, 1000);
```

We completely ripped out this simulation and replaced it with a real backend pipeline that refuses to report success unless the message genuinely reached its destination.

---

## 2. Plain-Words Explainer

### What a "Backend" Actually Is
A website running in your browser (the "frontend") is just paint on glass. It can draw boxes, format text, and animate buttons, but it has no memory and cannot send a letter by itself.
A "backend" is the server sitting behind the glass. It has real memory, can execute security rules that the visitor cannot tamper with, and has credentials to talk to external services (like email inboxes, databases, or webhook endpoints).

### What My Feature Does
When you type a message and hit **SEND MESSAGE**:
1. The browser bundles your inputs into a JSON envelope: `{"name": "...", "email": "...", "message": "...", "website": "..."}`.
2. The envelope is sent via an HTTP POST request to `/api/contact` on our server.
3. Our server validates the data:
   - Is `name` between 1 and 100 characters?
   - Is `email` a valid email format under 254 characters?
   - Is `message` at least 10 characters and under 5,000 characters?
   - Did a spam bot fill out the invisible `website` field (honeypot)? If so, answer with a fake `200 OK` so the bot learns nothing, but silently drop the payload.
   - Has this IP address sent more than 20 messages in the last hour? If so, return `429 Too Many Requests`.
4. If everything passes, the server forwards the message as an authenticated JSON webhook to the receiver (Formspree / Discord / Slack / Inbox).
5. If the receiver confirms receipt (`200-299`), our server responds to the browser with `{"ok": true}`. Only then does the green confirmation appear and the button change to **SEND ANOTHER**.
6. If the webhook is not configured or fails, the server returns an honest `503` or `502` error, telling the visitor to email directly rather than giving a false sense of security.

---

## 3. Evidence of Live Feature Working

### Automated E2E Verification
Executed via Playwright against the local server with a live HTTP receiver daemon (`http://127.0.0.1:5055/hook`):

```json
{"name": "Iris Vega", "email": "iris@example.com", "message": "Your triage demo worked on my messy inbox. Can we pilot this?", "source": "parthchawla.dev", "received_at": "2026-10-02T09:59:12.184912+00:00"}
```

- **Clean submission:** Delivered to receiver with timestamp and origin metadata.
- **Empty submission:** Rejected with `["name is required", "email is required", "message is required"]`.
- **Malformed email:** Rejected with `["that email address does not look right"]`.
- **Bot submission (honeypot filled):** Returns `200 OK` to caller, exactly 0 payloads forwarded to receiver.
- **Form reuse:** After successful send, the button becomes `SEND ANOTHER`, clears the form, and accepts a second valid message on the exact same page view without requiring a browser reload.

### Test Suite Output
```bash
$ .venv/bin/python -m pytest tests/test_contact.py -v
============================= test session starts ==============================
tests/test_contact.py::TestValidate::test_accepts_a_good_payload_and_trims_whitespace PASSED
tests/test_contact.py::TestValidate::test_rejects_a_payload_with_nothing_in_it PASSED
tests/test_contact.py::TestValidate::test_rejects_whitespace_only_fields PASSED
tests/test_contact.py::TestValidate::test_rejects_malformed_emails PASSED
tests/test_contact.py::TestValidate::test_rejects_an_over_long_email PASSED
tests/test_contact.py::TestValidate::test_rejects_a_too_short_message PASSED
tests/test_contact.py::TestValidate::test_rejects_a_too_long_message PASSED
tests/test_contact.py::TestValidate::test_rejects_an_over_long_name PASSED
tests/test_contact.py::TestValidate::test_rejects_a_non_object_body PASSED
tests/test_contact.py::TestValidate::test_never_echoes_the_submitted_content_back_in_errors PASSED
tests/test_contact.py::TestHoneypot::test_empty_honeypot_field_is_a_real_person PASSED
tests/test_contact.py::TestHoneypot::test_filled_honeypot_field_is_a_bot PASSED
tests/test_contact.py::TestRateLimiter::test_allows_up_to_the_limit_then_blocks PASSED
tests/test_contact.py::TestRateLimiter::test_counts_per_key_not_globally PASSED
tests/test_contact.py::TestRateLimiter::test_forgets_hits_once_the_window_passes PASSED
tests/test_contact.py::TestContactEndpoint::test_a_valid_submission_is_delivered_and_acknowledged PASSED
tests/test_contact.py::TestContactEndpoint::test_a_bot_filling_the_honeypot_is_answered_without_being_sent PASSED
tests/test_contact.py::TestContactEndpoint::test_an_invalid_submission_is_rejected_with_readable_reasons PASSED
tests/test_contact.py::TestContactEndpoint::test_it_never_claims_success_when_no_webhook_is_configured PASSED
tests/test_contact.py::TestContactEndpoint::test_it_reports_a_delivery_failure_instead_of_pretending PASSED
tests/test_contact.py::TestContactEndpoint::test_it_reports_an_unreachable_webhook_instead_of_pretending PASSED
tests/test_contact.py::TestContactEndpoint::test_it_throttles_a_human_who_double_submits_fast PASSED
tests/test_contact.py::TestContactEndpoint::test_it_ignores_a_body_that_is_not_json PASSED
============================== 26 passed in 0.28s ==============================
```
