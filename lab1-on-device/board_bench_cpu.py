"""Times a GGUF model on a plain CPU with llama-server. Works on the board and on the Mac.

Usage: python3 board_bench_cpu.py <llama-server path> <model.gguf>
"""
import json, subprocess, sys, time, urllib.request

SERVER, MODEL = sys.argv[1], sys.argv[2]
PORT = 8099
PROMPTS = {
    "short": "In one sentence, why do small AI models matter on devices?",
    "long": "Explain, for a product manager, the trade-offs between running an AI model on a device and in the "
            "cloud. Cover latency, privacy, cost and updates, and give one example of each. " * 4,
}

def rss_mb(pid):
    try:
        for line in open(f"/proc/{pid}/status"):
            if line.startswith("VmRSS"):
                return round(int(line.split()[1]) / 1024)
    except OSError:
        pass
    out = subprocess.run(["ps", "-o", "rss=", "-p", str(pid)], capture_output=True, text=True).stdout.strip()
    return round(int(out) / 1024) if out else None

start = time.time()
proc = subprocess.Popen([SERVER, "-m", MODEL, "--port", str(PORT), "-c", "4096", "--log-disable"],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
try:
    for _ in range(1800):
        try:
            if urllib.request.urlopen(f"http://127.0.0.1:{PORT}/health", timeout=1).status == 200:
                break
        except Exception:
            time.sleep(0.1)
    print(json.dumps({"cold_start_seconds": round(time.time() - start, 2), "memory_mb": rss_mb(proc.pid)}), flush=True)
    for name, prompt in PROMPTS.items():
        body = {"prompt": prompt, "n_predict": 128, "temperature": 0, "cache_prompt": False, "ignore_eos": True}
        req = urllib.request.Request(f"http://127.0.0.1:{PORT}/completion", json.dumps(body).encode(),
                                     {"content-type": "application/json"})
        t = json.load(urllib.request.urlopen(req, timeout=600))["timings"]
        print(json.dumps({"prompt": name, "prompt_tokens": t["prompt_n"],
                          "first_token_seconds": round(t["prompt_ms"] / 1000, 3),
                          "tokens": t["predicted_n"], "tokens_per_second": round(t["predicted_per_second"], 1)}), flush=True)
    print(json.dumps({"memory_mb_after": rss_mb(proc.pid)}))
finally:
    proc.terminate()
