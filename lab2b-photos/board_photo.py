"""Runs on the board. Puts each photo through a vision model on the MLA and saves the answers.

The server starts once and stays loaded. It takes an image as a file path on the board.
Usage: python3 board_photo.py <photo_eval.jsonl> <photos folder> <out.jsonl> [model]
"""
import json, os, re, subprocess, sys, time, urllib.request

EVAL, PHOTOS, OUT = sys.argv[1:4]
MODEL = sys.argv[4] if len(sys.argv) > 4 else "Qwen3-VL-4B-Instruct-GPTQ-a16w4"
URL = "http://127.0.0.1:9998/v1/chat/completions"
PROMPT = ("This is a photo from a security camera at a fenced site. A gate standing open, or a hole or "
          "cut in a fence, is a PROBLEM. Anything else is NORMAL, including objects left on the ground. "
          "Answer with one word, PROBLEM or NORMAL.")

def ask(path, tries=1):
    body = {"model": MODEL, "max_tokens": 8, "temperature": 0, "messages": [{"role": "user", "content": [
        {"type": "image_url", "image_url": {"url": path}}, {"type": "text", "text": PROMPT}]}]}
    req = urllib.request.Request(URL, json.dumps(body).encode(), {"content-type": "application/json"})
    t = time.time()
    out = json.load(urllib.request.urlopen(req, timeout=120))
    return out["choices"][0]["message"].get("content") or "", (time.time() - t) * 1000

log = open("photo_server.log", "w")
start = time.time()
proc = subprocess.Popen(["llima", "run", "--mode", "web", MODEL], stdout=log, stderr=log)
try:
    while "listening on port" not in open("photo_server.log", errors="replace").read():
        if proc.poll() is not None or time.time() - start > 180:
            raise SystemExit("server did not start, see photo_server.log")
        time.sleep(0.5)
    time.sleep(1)
    print(f"cold start {time.time() - start:.1f} s", flush=True)
    rows = [json.loads(l) for l in open(EVAL)]
    with open(OUT, "w") as f:
        for i, r in enumerate(rows, 1):
            text, ms = ask(os.path.join(PHOTOS, r["file"]))
            found = re.findall(r"\b(PROBLEM|NORMAL)", text.upper())
            r.update(model=MODEL, answer=found[0].lower() if found else "UNPARSED", text=text[:80], ms=ms)
            f.write(json.dumps(r) + "\n"); f.flush()
            print(f"{i}/{len(rows)}  {r['answer']:<9} {ms:.0f} ms  {text[:30]!r}", flush=True)
    print("saved", OUT)
finally:
    proc.kill()
