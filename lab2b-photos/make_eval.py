"""Builds data/photo_eval.jsonl from the real photos and whichever generated images exist.

A box in front of an undamaged gate is labelled normal: something changed, but nothing is damaged.
Usage: python3 lab2b-photos/make_eval.py
"""
import json, os, re

ROOT = "data/site_photos"
rows = json.load(open(f"{ROOT}/real/meta.json"))
for name in sorted(os.listdir(f"{ROOT}/generated")):
    m = re.fullmatch(r"(box|clear|cut)-(\d+)\.(png|jpe?g|webp)", name)
    if m:
        rows.append({"id": f"gen-{m[1]}-{m[2]}", "file": f"generated/{name}", "group": f"generated_{m[1]}",
                     "label": "problem" if m[1] == "cut" else "normal", "truth": m[1]})
with open("data/photo_eval.jsonl", "w") as f:
    for r in rows:
        f.write(json.dumps(r) + "\n")
print(len(rows), "rows:", {g: sum(r["group"] == g for r in rows) for g in sorted({r["group"] for r in rows})})
