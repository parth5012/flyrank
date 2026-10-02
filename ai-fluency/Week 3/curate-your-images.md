# Week 3 · Kill Your Darlings: Curate Your Images

**Date:** 2026-09-07  
**Track:** AI Fluency · AI n-able Yourself

---

## 1. Curated Image List (The 4 Images That Actually Serve The Claim)

Because the portfolio claim is *"I build AI systems that keep working on messy real data because I measure them"*, screenshots of mockups, stock photos of servers, and generic AI illustrations were completely eliminated. Every visual artifact must represent raw verification or system identity.

| Asset | Path | Format | Why It Is Essential |
|---|---|---|---|
| **Social Share Card (Open Graph)** | `static/og.png` | 1200×630 PNG | The first impression when sharing the site link on LinkedIn, X, or Slack. Shows the one claim, dark telemetry grid, and the `/reliability` badge. |
| **Site Favicon** | `static/favicon.ico` | 32×32 ICO | Visual anchor in the browser tab bar, preventing default browser 404s. |
| **Hero Code Block / Telemetry Graphic** | Generated in DOM via CSS & SVG | Native SVG / HTML | Shows the live `what_breaks.txt` file and terminal dot status without downloading bulky PNG assets. Fast, responsive, crisp on all DPIs. |
| **FlyRank Graduate Badge** | Footer SVG / PNG | Vector / PNG | Third-party credential verification linking directly to the accredited internship proof page. |

---

## 2. Ruthlessly Rejected Images (Killed Darlings)

1. **Rejected: Full-page website screenshots of old projects (Artify Bharat & EdTech Dashboard)**
   - *Why rejected:* They showed UI screens of e-commerce storefronts and interview tools. While visually colorful, they completely distracted from the backend AI reliability claim. A founder evaluating an email triage or automated classifier does not care about artisan e-commerce UI design.
2. **Rejected: Generic AI brain / neon circuit stock photo**
   - *Why rejected:* Dilutes authenticity. Stock imagery screams "student project with no real code." Replaced with clean CSS grid lines and monospace code windows.
3. **Rejected: Casual portrait selfie / lifestyle headshot**
   - *Why rejected:* Low contrast with the dark theme; did not communicate technical rigor. Replaced with the clean geometric vector monogram avatar in the personnel file.

---

## 3. Honest Note on a Rejected Image

> **The rejected image:** A high-resolution graphic of the "Artify Bharat Artisan Portal" featuring product cards and artisan profiles.  
> **Why it was tempting:** It was the most visually complex thing I had built, took weeks to style in Tailwind, and looked like a commercial product.  
> **Why it had to die:** It actively hurt the story. It made me look like an aspiring full-stack React frontend contractor rather than an engineer who ensures AI pipelines don't fail on messy data. Cutting my most "visually impressive" screen was uncomfortable, but keeping it would have split the site into two conflicting claims.
