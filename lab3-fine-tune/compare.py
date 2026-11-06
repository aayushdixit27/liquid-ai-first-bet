"""Compare two chat-model runs on the same eval rows. Usage: python3 compare.py before.jsonl after.jsonl"""
import collections, json, sys

load = lambda p: {r["id"]: r for r in map(json.loads, open(p))}
before, after = load(sys.argv[1]), load(sys.argv[2])
if before.keys() != after.keys():
    raise SystemExit("These runs used different rows, so they can't be compared.")
leak = lambda r: r["label"] == "leak"
right = lambda r: (r["chat"] == "LEAK") == leak(r) and r["chat"] != "UNPARSED"

def line(name, rows):
    rows = list(rows.values())
    print(f"{name:<8} right {sum(map(right, rows)):>2}/{len(rows)}   leaks missed {sum(leak(r) and not right(r) for r in rows):>2}"
          f"   safe blocked {sum(not leak(r) and not right(r) for r in rows):>2}   unparsed {sum(r['chat'] == 'UNPARSED' for r in rows)}")

line("before", before); line("after", after)
changed = sum(before[i]["chat"] != after[i]["chat"] for i in before)
rows = list(after.values())
print(f"\nAnswers that changed: {changed} of {len(rows)}. Two equal scores can hide this.")
print(f"Doing nothing, always answering SAFE, would score {sum(not leak(r) for r in rows)}/{len(rows)}.")
if all("rules" in r for r in rows):
    both = sum((r["rules"] or r["chat"] == "LEAK") == leak(r) for r in rows)
    print(f"Rules, then this model: right {both}/{len(rows)}.")
fresh = {i: r for i, r in after.items() if r.get("unseen_secret")}
if fresh:
    print("\nThe honest test: only rows whose secret never appeared in training")
    line("before", {i: before[i] for i in fresh}); line("after", fresh)
print("\nBy category, right before -> after:")
cats = collections.defaultdict(lambda: [0, 0, 0])
for i, r in before.items():
    c = cats[r["category"]]; c[0] += 1; c[1] += right(r); c[2] += right(after[i])
for k, (n, b, a) in sorted(cats.items()):
    print(f"  {k:<26} {b}/{n} -> {a}/{n}")
print("\nStill wrong after:")
for r in after.values():
    if not right(r):
        print(f"  said {r['chat']:<8} truth {r['label']:<5} {r['category']:<20} {r['reply'][:60]!r}")
