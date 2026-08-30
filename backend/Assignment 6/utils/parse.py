import  re

def extract_json(raw: str) -> str:
    raw = raw.strip()
    # strip code fence
    m = re.search(r"```(?:json)?\s*(.*?)\s*```", raw, re.DOTALL)
    if m: raw = m.group(1)
    # find first { ... last }
    start = raw.find("{")
    end = raw.rfind("}")
    if start != -1 and end != -1:
        raw = raw[start:end+1]
    return raw

# alias required by spec: format_json
def format_json(raw: str) -> str:
    return extract_json(raw)
