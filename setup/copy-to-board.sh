#!/bin/bash
# Copies everything the labs need onto the board. The board has no internet, so files go over the cable.
set -e
cd "$(dirname "$0")/.."
B=sima@192.168.1.20
ssh $B 'mkdir -p /media/nvme/labs/models /media/nvme/labs/scripts'
scp lab1-on-device/board_*.py lab2-decide/board_*.py data/judge_eval.jsonl $B:/media/nvme/labs/scripts/ 2>/dev/null || true
ssh $B 'ls /media/nvme/llima/models/LFM2.5-230M-a16w4 >/dev/null 2>&1' || scp -r .cache/models/sima/LFM2.5-230M-a16w4 $B:/media/nvme/llima/models/
scp -q .cache/models/LFM2.5-230M-GGUF/*Q8_0*.gguf $B:/media/nvme/labs/models/
[ -f .cache/board/llama-server ] && scp -q .cache/board/llama-server $B:/media/nvme/labs/ || echo "No board llama-server yet: run setup/build-llama-for-board.sh first. Lab 1 steps on the accelerator still work."
[ -f .cache/models/d1-2B-GGUF/d1-2B-Q4_K_M.gguf ] && scp -q .cache/models/d1-2B-GGUF/d1-2B-Q4_K_M.gguf $B:/media/nvme/labs/models/
# Photo test: photos, eval rows and the script. Run lab2b-photos/make_eval.py first.
scp -q lab2b-photos/board_photo.py data/photo_eval.jsonl $B:/media/nvme/labs/scripts/ 2>/dev/null || true
scp -q -r data/site_photos $B:/media/nvme/labs/ 2>/dev/null || true
[ -d .cache/models/sima/LFM2.5-VL-450M-Autoround-a16w4 ] && { ssh $B 'ls /media/nvme/llima/models/LFM2.5-VL-450M-Autoround-a16w4 >/dev/null 2>&1' || scp -q -r .cache/models/sima/LFM2.5-VL-450M-Autoround-a16w4 $B:/media/nvme/llima/models/; }
ssh $B 'df -h /media/nvme | tail -1; ls -la /media/nvme/labs /media/nvme/labs/models; llima list'
