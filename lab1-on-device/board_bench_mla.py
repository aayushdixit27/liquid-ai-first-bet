"""Runs on the board. Times a model on the MLA accelerator through the llima command-line tool.

Usage: python3 board_bench_mla.py LFM2.5-230M-a16w4
Prints one JSON line per prompt and saves llima's raw output next to this script.
"""
import json, os, pty, re, select, subprocess, sys, time

MODEL = sys.argv[1] if len(sys.argv) > 1 else "LFM2.5-230M-a16w4"
PROMPTS = {
    "short": "In one sentence, why do small AI models matter on devices?",
    "long": "Explain, for a product manager, the trade-offs between running an AI model on a device and in the "
            "cloud. Cover latency, privacy, cost and updates, and give one example of each. " * 4,
}
master, slave = pty.openpty()
start = time.time()
proc = subprocess.Popen(["llima", "run", "--mode", "cli", MODEL], stdin=slave, stdout=slave, stderr=slave, close_fds=True)
os.close(slave)
buf = ""

def read_until(pattern, timeout):
    global buf
    end = time.time() + timeout
    while time.time() < end:
        m = re.search(pattern, buf, re.S)
        if m:
            return m
        r, _, _ = select.select([master], [], [], 0.2)
        if r:
            try:
                buf += os.read(master, 4096).decode("utf-8", "replace")
            except OSError:
                break
    return None

raw = ""
if read_until(r">>> ", 180) is None:
    proc.kill()
    print(json.dumps({"model": MODEL, "error": "model did not start", "output": buf[-800:]}))
    sys.exit(1)
load_s = time.time() - start
raw += buf
print(json.dumps({"model": MODEL, "cold_start_seconds": round(load_s, 2)}), flush=True)
for name, prompt in PROMPTS.items():
    buf = ""
    t0 = time.time()
    os.write(master, (prompt + "\n").encode())
    first = read_until(r"Assistant:\s*\S", 120)
    ttft = time.time() - t0 if first else None
    done = read_until(r"Number of generated tokens[^\n]*\n", 180)
    total = time.time() - t0
    raw += buf
    tokens = None
    if done:
        n = re.search(r"Number of generated tokens\D*(\d+)", buf)
        tokens = int(n.group(1)) if n else None
    speed = round(tokens / (total - ttft), 1) if tokens and ttft and total > ttft else None
    print(json.dumps({"model": MODEL, "prompt": name, "first_token_seconds": round(ttft, 2) if ttft else None,
                      "total_seconds": round(total, 2), "tokens": tokens, "tokens_per_second": speed,
                      "llima_says": (re.findall(r"[^\n]*(?:token|Token)[^\n]*", buf) or [""])[-3:]}), flush=True)
    read_until(r">>> ", 10)
proc.kill()
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f"raw_{MODEL}.txt"), "w").write(raw)
