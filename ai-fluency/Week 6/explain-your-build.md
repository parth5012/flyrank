# Week 6 · Explain It Like You Built It

**Date:** 2026-09-28  
**Track:** AI Fluency · AI n-able Yourself

---

## The Part I Picked: In-Memory Sliding-Window Rate Limiting

In `contact.py`, we implemented a rate limiter to prevent double-click submit storms and bot abuse without introducing an external database like Redis:

```python
class RateLimiter:
    def __init__(self, limit=20, window_seconds=3600):
        self.limit = limit
        self.window_seconds = window_seconds
        self._hits = {}
        self._lock = threading.Lock()

    def allow(self, key, limit=None):
        now = time.monotonic()
        cutoff = now - self.window_seconds
        cap = self.limit if limit is None else limit
        with self._lock:
            hits = deque(t for t in self._hits.get(key, ()) if t > cutoff)
            if len(hits) >= cap:
                self._hits[key] = hits
                return False
            hits.append(now)
            self._hits[key] = hits
            return True
```

---

## Explained in Plain Words (Like Teaching a Friend)

Imagine you are standing at the entrance to a movie theater, and the rule is: *"Nobody can enter more than 20 times in any single hour."*

Here is how you would enforce this without an expensive computer:
1. You have a notebook. Every time a person (identified by their IP address) walks in, you look at your stopwatch and write down the exact minute they arrived right under their name.
2. An hour later, when that same person tries to enter again, you don't just count all the checkmarks under their name forever. You draw a line through any timestamp that is older than 60 minutes ago. Those don't count anymore—they happened in the past.
3. If they still have 20 recent timestamps on the page, you stop them and say: *"Too many visits; please wait."* If they have 19 or fewer, you write down the current time, let them through, and smile.

### Why this specific code is interesting:
- **`time.monotonic()` instead of `time.time()`:** Clock time can jump backwards if your computer syncs with an internet time server (NTP). If you used clock time, someone could submit 50 messages during a time sync and slip right through. `time.monotonic()` is like a physical stopwatch that can only tick forwards; it never jumps backwards.
- **`collections.deque`:** A deque ("double-ended queue") is a fast Python list designed to drop old items from the left and add new ones to the right in constant time $O(1)$.
- **`threading.Lock()`:** If two visitors click "Submit" at the exact same millisecond, two threads in Python might try to read the notebook at once and both see "19 visits," letting both through (21 total). The `Lock` forces them to take turns reading and writing to the notebook.

### What it cannot do (The honest limitation):
Because this notebook lives in the computer's temporary memory (RAM), if the Vercel serverless container restarts or a second container spins up in a different data center, each container gets its own fresh notebook. That is why it is listed on `/reliability` as a known limitation: it stops rapid spam bursts from an individual user, but is not a global distributed firewall.
