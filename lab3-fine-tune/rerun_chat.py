"""Re-run only the small chat model on the Mac, using CHAT_HINT if it's set.

Usage: python3 rerun_chat.py <unused> <out.jsonl> [model.gguf] [rows.jsonl]
"""
import shutil, subprocess, sys

model = sys.argv[3] if len(sys.argv) > 3 else ".cache/models/LFM2.5-230M-GGUF/LFM2.5-230M-Q8_0.gguf"
subprocess.run([sys.executable, "lab2-decide/board_judge.py", shutil.which("llama-server"), "skip", model,
                sys.argv[4] if len(sys.argv) > 4 else "data/judge_eval.jsonl", sys.argv[2]], check=True)
