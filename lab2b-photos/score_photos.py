"""Scores saved photo answers. Usage: python3 lab2b-photos/score_photos.py results.jsonl"""
import json, statistics, sys

rows = [json.loads(l) for l in open(sys.argv[1])]

def line(name, rs):
    if not rs:
        return
    right = sum(r["answer"] == r["label"] for r in rs)
    missed = sum(r["label"] == "problem" and r["answer"] != "problem" for r in rs)
    false = sum(r["label"] == "normal" and r["answer"] != "normal" for r in rs)
    print(f"{name:<20} right {right:>2}/{len(rs):<3} problems missed {missed:>2}   false alarms {false:>2}")

print(rows[0]["model"], f"median {statistics.median(r['ms'] for r in rows):.0f} ms per photo")
line("all", rows)
for g in sorted({r["group"] for r in rows}):
    line(g, [r for r in rows if r["group"] == g])
print(f"unparsed: {sum(r['answer'] == 'UNPARSED' for r in rows)}")
print("\nWrong:")
for r in rows:
    if r["answer"] != r["label"]:
        print(f"  {r['id']:<20} truth {r['label']:<8} said {r['answer']:<9} {r['text']!r}")
