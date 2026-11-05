---
name: lab1
description: Guides Aayush through Lab 1, running Liquid models on the Modalix board's accelerator and CPU. Use on /lab1.
---

# Lab 1: on-device

**Interview gap this closes:** "when is an on-device model the right tool?" and "when is an LFM the right tool?" They should finish able to answer with numbers they measured themself. It also starts the bet that runs through all three labs: picks where to play, and thesis then evidence.

All lab commands run from the repo folder, so if you're in its parent, start with `! cd liquid-ai-first-bet`.

Read `LABGUIDE.md` in the repo root first and follow it. It sets how to guide.

Target: 60 minutes.

## Step 0. Place the bet (5 min)

Have them write `BET.md`: one vertical, one use case, who buys it, why now, and a claim that could be proven wrong. Good form: "A model that fits on this board can do X fast enough for Y. I'm wrong if Z." Don't let them leave it vague. This lab tests the "fits and is fast enough" part.

## Step 1. Connect (5 min)

Have them plug the board in, power it on, and wait about 60 seconds. Connect the USB Ethernet adapter. It should appear as `en8`.

```
ping -c1 192.168.1.20
ssh sima@192.168.1.20 'nproc; free -h | head -2; llima list'
```

Point out 16 cores and 5.8 GiB of memory. The vendor says 16 GB; the rest is reserved for the accelerator and camera pipeline. That's why "does it fit" is the first product question on-device.

If the Mac can't reach it, `setup.md` in the Senso knowledge base has the recovery steps. The Mac side must be `192.168.1.10`, and `nmcli connection up end0-static` over serial brings the board back.

## Step 2. Copy files (5 min)

```
./setup/copy-to-board.sh
```

The board has no internet, so models travel over the cable. Say why that's a feature: it's the data-sovereignty story made physical.

## Step 3. Talk to it (5 min)

**Concept:** a CPU does anything, one instruction at a time. An accelerator (the MLA here) does one kind of math very fast at low power, but only runs models compiled for it in advance.

```
ssh -t sima@192.168.1.20 'llima run LFM2.5-230M-a16w4'
```

This is a 230-million-parameter Liquid model on the accelerator. Have them ask it five things, including something it should fail at. Ask what surprised them. A model this small is fast and often wrong; that's the point of the lab.

## Step 4. Measure the accelerator (10 min)

Prediction first: SiMa's card says 279.9 tokens per second and 0.01 s to first token. Will they hit it?

```
ssh sima@192.168.1.20 'cd /media/nvme/labs/scripts && python3 board_bench_mla.py LFM2.5-230M-a16w4'
```

Output: `cold_start_seconds`, `first_token_seconds`, `tokens_per_second`.

If `tokens` is null, the script couldn't read llima's output. Open `/media/nvme/labs/scripts/raw_LFM2.5-230M-a16w4.txt`, find the real format, and fix the regex together.

The script's speed is wall-clock across a terminal, so it will read a bit lower than SiMa's number. Say so, and don't call it a gap in SiMa's claim unless it's large.

## Step 5. Measure the same model on the CPU (10 min)

Skip this step if `.cache/board/llama-server` isn't on the board, and tell them it was skipped.

**Concept:** the same model, as a GGUF file, running on the plain CPU through llama.cpp. llama.cpp is a free program that runs AI models on ordinary computers.

```
ssh sima@192.168.1.20 'cd /media/nvme/labs/scripts && python3 board_bench_cpu.py /media/nvme/labs/llama-server /media/nvme/labs/models/LFM2.5-230M-Q8_0.gguf'
```

Compare with step 4. How much does the accelerator buy? Note that the two aren't identical: different quantization and different runtime.

## Step 6. A bigger model, and cold start (10 min)

```
ssh sima@192.168.1.20 'cd /media/nvme/labs/scripts && python3 board_bench_mla.py Qwen3-VL-4B-Instruct-GPTQ-a16w4'
```

Earlier work found about 22 tokens per second and about 20 seconds per call, mostly loading.

**This is the most useful number in the lab.** Ask: what's the user experience of a 20-second cold start? What would you change, the model or the harness? Answer: keep the model loaded, which is a harness fix and no model change.

Also check that nothing left the board:

```
ssh sima@192.168.1.20 'cat /sys/class/net/end0/statistics/tx_bytes'
```

## Step 7. Write it down, update the bet (10 min)

Fill `lab1-on-device/RESULTS.md` with their numbers, using the template in `LABGUIDE.md`. Then have them answer, out loud, in 60 seconds:

1. When is on-device the right call, and when is it a mistake?
2. What's the difference between a model that's fast and a model that's useful?
3. LFM3 and d1 can't run on this accelerator today. Why does that matter to Liquid, and what would they ask for?

Then update `BET.md`: did these numbers support it, change it or kill it? Name the buyer, budget owner and a first guess at pricing. What would they cut?

**What to take away:** 230M is very fast on this chip and weak at hard tasks. 4B is slower and smarter. LFM3 and d1 run only on this board's CPU, because no compiled version exists. So "the right tool" depends on what fits and what the chip supports, as well as on accuracy.

Then update the coach, as `LABGUIDE.md` says.
