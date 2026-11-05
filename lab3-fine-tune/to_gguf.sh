#!/bin/bash
# Turns a trained model folder into one GGUF file that llama.cpp can run. About 2 minutes.
set -e
cd "$(dirname "$0")/.."
SRC="${1:-runs/tuned}"
[ -d .cache/llama.cpp ] || git clone -q --depth 1 --branch b12128 https://github.com/ggml-org/llama.cpp .cache/llama.cpp
.venv/bin/python .cache/llama.cpp/convert_hf_to_gguf.py "$SRC" --outtype f16 --outfile runs/tuned-f16.gguf
llama-quantize runs/tuned-f16.gguf runs/LFM2.5-230M-tuned-Q8_0.gguf Q8_0
rm runs/tuned-f16.gguf
ls -la runs/LFM2.5-230M-tuned-Q8_0.gguf
