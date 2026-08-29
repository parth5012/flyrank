import random, time
from openai import APIStatusError, APITimeoutError, APIConnectionError

RETRYABLE = {429, 500, 502, 503, 504}

def call_with_retry(fn):
  delays = [1.0, 2.0, 4.0]  # exp backoff + jitter
  for i, d in enumerate(delays + [None]): # 3 retries max = 4 attempts total -> last None = no sleep
    try:
      return fn()
    except APITimeoutError as e:
      if i == 3: raise
    except APIConnectionError as e:
      if i == 3: raise
    except APIStatusError as e:
      if e.status_code in (400,401,403): raise  # never retry
      if e.status_code not in RETRYABLE: raise
      if e.status_code == 429 and e.response.headers.get("Retry-After"):
        time.sleep(float(e.response.headers["Retry-After"]))
        continue
      if i == 3: raise
    time.sleep(d + random.uniform(0, 0.5))