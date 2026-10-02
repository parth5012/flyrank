# Week 7 · Open It On Your Phone — fix log

**Assignment:** fix what breaks on a real phone first, then readability, speed and every link.

**Method:** every page rendered and inspected at **390 × 844** (iPhone 14 class viewport) as well
as 1280px, with automated checks for horizontal overflow and console errors on all seven routes.

Pages tested: `/`, `/projects`, `/projects/classify`, `/reliability`, `/contact`, `/about`,
`/blog`.

---

## Fixes made (in order found)

### 1. Page-specific CSS rendered as visible text — *fix-now, shipped*

The worst bug, and it would have been visible to any reviewer. When the Tailwind Play CDN
`<script>` and its inline config were removed, the `{% block extra_styles %}` hook in
`base.html` was left **outside** the `<style>` wrapper that used to contain it. Every page was
therefore printing its own stylesheet as body copy above the navigation — a wall of raw CSS at
the top of all seven pages.

Fixed by restoring the `<style>` wrapper around the block. This is the reason I render and
*screenshot* pages rather than only checking HTTP status: every route still returned `200` while
looking completely broken.

### 2. The contact script died on every page load — *fix-now, shipped*

Console error on `/contact`:

```
SyntaxError: Identifier 'btn' has already been declared
```

`base.html` and `contact.html` each declared a top-level `const btn` in their own `<script>`
block. Both are global scope, so the second one to load threw and the entire contact handler
never attached — the form would have done nothing on submit.

Fixed by wrapping the contact script in an IIFE and renaming its bindings.

### 3. Featured case cards were crushed on a phone — *fix-now, shipped*

The featured case card carried a hardcoded inline style:

```html
<div class="project-card lg:flex-row" style="flex-direction:row; display:flex;">
```

The inline `flex-direction: row` **overrides** the responsive `lg:` utility, so at 390px the
body copy and the graphic panel were still side by side, each about half the screen width. Text
was wrapping to three and four words a line.

Fixed by dropping the inline style and using `flex flex-col lg:flex-row` on both the home and
work pages.

### 4. Scroll indicator overlapped the stat cards — *fix-now, shipped*

The "SCROLL" cue was absolutely positioned at `bottom-8` inside a hero that is taller than the
viewport on mobile, so it landed on top of the third stat tile. Removed it; it was decoration
that was actively covering data.

### 5. Submit button became permanently unusable — *fix-now, shipped*

Found by driving the real form in a browser rather than by unit test. After one successful
send the button got `hidden` and the form could not be used again without a page reload. It now
switches to **SEND ANOTHER** and stays usable. A second message from the same visitor now works.

### 6. Rate limit too tight for shared IPs — *fix-now, shipped*

`5` submissions per `600` seconds, keyed by IP. Mobile carriers and office Wi-Fi put many real
people behind one address, so a legitimate visitor sharing a network could lock themselves out
after five messages. Raised to `20` per `3600` seconds. The limit still stops a double-submit
storm or a naive script, which is all it is for.

### 7. One fact value wrapped to two lines on a phone — *fix-now, shipped*

`"3, jittered"` broke across lines inside a narrow fact tile. Changed to `"3x"` and the label
carries the detail.

---

## Readability

- All body copy is at least `1.02rem` with `1.75` line-height in long-form blocks.
- Every page has exactly one `h1`.
- Mobile menu is a labelled button with `aria-expanded` and `aria-controls`, and the nav is
  wrapped in `<nav aria-label>`, so the toggle is announced rather than being a mystery hamburger.
- A skip link (`Skip to content`) is the first focusable element on every page.
- Focus rings are visible (`outline: 2px solid #38dafa`) instead of removed.
- `prefers-reduced-motion` disables the page-entry animation and smooth scrolling.
- Decorative icon-only links carry `aria-label` (GitHub, LinkedIn, email).

## Links

Every internal route returns `200`; `/skills` and `/resume` redirect as designed; an unknown case
slug returns `404` through the existing error handler rather than a stack trace. External links
(GitHub, LinkedIn, the five source repositories) were checked against the live repositories so no
link points at a case study that does not exist.

## Result

All seven pages: **no horizontal overflow at 390px, no console errors.** The only network error
in the test harness is the blocked webfont request, which the harness does deliberately so
screenshots render deterministically.

## Known limitation

I tested one mobile viewport class (390px) and one desktop (1280px), plus the browser default
engine. I did not test a physical iOS or Android device, and I did not test Safari or Firefox.
The site uses no browser-specific CSS, but "I checked in Chromium at two widths" is the accurate
claim and I am not going to write it up as broader than it is.