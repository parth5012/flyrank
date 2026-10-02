# Build-in-Public Launch Story

*Copy for LinkedIn / X / FlyRank Showcase and published on the live site at `/blog`.*

---

## How I built my portfolio with AI, and the part that lied to me

I started with a site that looked finished and proved nothing. It had three projects, a typewriter animation on my name, and a headline asking for an internship. I had spent weeks on the wrong thing: decorating a page instead of proving a claim.

So I did the unglamorous part first. I wrote one sentence I could actually defend: that I build AI systems which keep working on messy real data because I measure them instead of guessing. Then I threw away the three projects that couldn't support it, replacing them with five cases pulled directly from my codebases—each with its eval sets, quarantine logs, and honest failures.

**What AI did that I could not have done alone:** It wrote the code. The Jinja templates, the compiled Tailwind pipeline, the Flask contact endpoint with server-side validation and rate limiting, and all 26 tests behind it. I wrote none of that boilerplate by hand. That speed bought me the time to do what actually matters: writing the eval sets, deciding what to leave out, and choosing to publish the embarrassing findings instead of burying them.

**And here is the part that broke:** My contact form lied to me.

The original JavaScript used `setTimeout()` to display a green "Message sent!" checkmark after 1,000ms. No server call. No webhook. It dropped every message on the floor while reassuring the visitor. A stranger would have trusted it.

I only caught it because I attacked my own site on purpose. That failure is now permanently documented on `/reliability` alongside our known limitations.

The lesson wasn't that AI is unreliable. It was that a plausible demo path is the exact thing an AI will cheerfully build for you. The only defense is trying to break your own work before someone else does.

Live portfolio: https://portfolio-kappa-ashy-3sqgkdkyxc.vercel.app  
Source & eval harnesses: https://github.com/parth5012/flyrank
