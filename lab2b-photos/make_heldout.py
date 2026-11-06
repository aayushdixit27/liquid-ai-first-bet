"""Builds a gate test from the dataset photos the first test didn't use, so the new claim gets a clean score.

The photos stay in .cache and go to the board over the cable. Usage: python3 lab2b-photos/make_heldout.py
"""
import glob, hashlib, json, os, shutil, subprocess

digest = lambda p: hashlib.md5(open(p, "rb").read()).hexdigest()
used = {digest(p) for p in glob.glob("data/site_photos/real/*.jpg")}
out = ".cache/heldout/heldout"
os.makedirs(out, exist_ok=True)
rows, seen = [], set()
for truth, label in (("open", "problem"), ("closed", "normal")):
    for path in sorted(glob.glob(f".cache/datasets/gate/*/{truth}/*")):
        d = digest(path)
        if d in used or d in seen:
            continue
        seen.add(d)
        name = f"{truth}-{len(rows):03d}.jpg"
        shutil.copy(path, f"{out}/{name}")
        rows.append({"id": name[:-4], "file": f"heldout/{name}", "label": label, "group": f"heldout_{truth}", "truth": truth})
with open("data/photo_heldout.jsonl", "w") as f:
    for r in rows:
        f.write(json.dumps(r) + "\n")
print(len(rows), "rows,", sum(r["label"] == "normal" for r in rows), "closed. Always answering NORMAL scores that many.")
