#!/usr/bin/env python3
# Pitfall injector: turn your pitfall notes into a standard pitfall-library entry + hook injection snippet
# Usage: python3 pitfall_inject.py my_pitfalls.md >> pitfall_library.md
# Input format is loose: any markdown containing any subset of the sections "title / symptom / cause / fix"
import sys, re, datetime

def section(text, *names):
    for n in names:
        m = re.search(rf"(?:^|\n)#+\s*{n}[^\n]*\n(.*?)(?=\n#+\s|\Z)", text, re.S)
        if m: return m.group(1).strip()
    return ""

def main():
    raw = open(sys.argv[1], encoding="utf-8").read()
    title = (re.search(r"^#\s*(.+)$", raw, re.M) or [None, sys.argv[1]])[1].strip()
    symptom = section(raw, "Symptom", "Symptoms", "Problem", "\u73b0\u8c61", "\u75c7\u72b6", "\u95ee\u9898") or raw.split("\n", 1)[1][:200]
    cause = section(raw, "Cause", "Reason", "\u6839\u56e0", "\u539f\u56e0") or "[to be filled]"
    fix = section(raw, "Fix", "Prevention", "Solution", "Countermeasure", "\u600e\u4e48\u9632", "\u9884\u9632", "\u89e3\u6cd5", "\u5bf9\u7b56") or "[to be filled]"
    today = datetime.date.today().isoformat()
    entry = f"""
## {title} ({today})
- Symptom: {symptom[:300]}
- Cause: {cause[:300]}
- Fix: {fix[:300]}
"""
    inject = f"- [Pitfall] {title[:60]}: {fix[:120]}"
    print(entry)
    print("---hook injection snippet (paste at the end of a task book / ruleset)---")
    print(inject)

if __name__ == "__main__":
    main()
