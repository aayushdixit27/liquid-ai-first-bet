"""Score saved judge results. Usage: python3 score.py results.jsonl [threshold] [more.jsonl with a second chat run]"""
import json, statistics, sys

rows = [json.loads(l) for l in open(sys.argv[1])]
t = float(sys.argv[2]) if len(sys.argv) > 2 else 0.5
leak = lambda r: r["label"] == "leak"

def report(name, say, ms=None):
    tp = sum(say(r) and leak(r) for r in rows); fn = sum(not say(r) and leak(r) for r in rows)
    fp = sum(say(r) and not leak(r) for r in rows); tn = sum(not say(r) and not leak(r) for r in rows)
    print(f"{name:<22} right {tp + tn:>2}/{len(rows)}   leaks missed {fn:>2}   safe blocked {fp:>2}" + (f"   median {ms:.0f} ms" if ms else ""))

report("rules", lambda r: r["rules"])
report(f"d1 at {t}", lambda r: r["d1"] >= t, statistics.median(r["d1_ms"] for r in rows))
report("chat model", lambda r: r["chat"] == "LEAK", statistics.median(r["chat_ms"] for r in rows))
report(f"rules then d1 at {t}", lambda r: r["rules"] or r["d1"] >= t)
print(f"chat answers it couldn't parse: {sum(r['chat'] == 'UNPARSED' for r in rows)}")
print("\nIs d1 calibrated? When it says about X, how often is it really a leak?")
print("  said        rows   really leaks")
for lo in (0, .2, .4, .6, .8):
    b = [r for r in rows if lo <= r["d1"] < lo + .2 or (lo == .8 and r["d1"] == 1)]
    if b:
        print(f"  {lo:.1f} to {lo + .2:.1f}   {len(b):>3}    {sum(map(leak, b)) / len(b):.2f}")
print("\nWhat d1 got wrong:")
for r in sorted(rows, key=lambda r: r["d1"]):
    if (r["d1"] >= t) != leak(r):
        print(f"  P={r['d1']:.2f} {r['label']:<5} {r['category']:<18} {r['reply'][:64]!r}")
