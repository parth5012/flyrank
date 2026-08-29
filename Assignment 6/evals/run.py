import json, pathlib, sys
import httpx

CASES = pathlib.Path(__file__).with_name("cases.json")
BASE = "http://localhost:8000"

def main():
    cases = json.loads(CASES.read_text(encoding="utf-8"))
    passed = 0
    failures = []
    for c in cases:
        r = httpx.post(f"{BASE}/classify", json={"text": c["text"]}, timeout=35)
        if r.status_code != 200:
            failures.append({"id": c["id"], "text": c["text"], "expected": c["expected"]["category"], "got": f"HTTP {r.status_code}", "body": r.text})
            continue
        got = r.json().get("category")
        exp = c["expected"]["category"]
        if got == exp:
            passed += 1
        else:
            failures.append({"id": c["id"], "text": c["text"], "expected": exp, "got": got, "full": r.json()})
    total = len(cases)
    pct = 100 * passed / total if total else 0
    print(f"Eval: {passed}/{total} ({pct:.0f}%) on category")
    if failures:
        print("Failures:")
        for f in failures:
            print(json.dumps(f, ensure_ascii=False))
    else:
        print("All matched.")

if __name__ == "__main__":
    main()
