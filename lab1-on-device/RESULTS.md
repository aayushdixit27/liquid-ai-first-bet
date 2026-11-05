# Lab 1: On-device

Built with Claude to prepare for my Liquid AI product interview. I ran it on my own SiMa Modalix board.

## What I wanted to know

When does a model belong on the device, and does a model that fits on this board run fast enough for my bet?

## What I measured

| What | Number | Label | Limit |
|---|---|---|---|
| Stated memory | 16 GB | vendor | |
| Memory Linux sees | 5.8 GiB | measured | One reading |
| Memory available | 5.3 GiB | measured | Board idle |
| 230M on accelerator, stated speed | 279.9 tokens/s | vendor | |
| 230M on accelerator, stated first token | 0.01 s | vendor | Prompt length not known |
| 230M on accelerator, cold start | 3.03 s | measured | One run |
| 230M on accelerator, long prompt speed | 279.3 tokens/s | measured | One run, 329 tokens |
| 230M on accelerator, long prompt first token | 0.04 s | measured | Timed across a terminal |
| 230M on accelerator, short prompt speed | 297.1 tokens/s | measured | One run, 35 tokens, too short to trust |
| 230M on accelerator, short prompt first token | 0.02 s | measured | Timed across a terminal |
| 230M on CPU, cold start | 2.46 s | measured | One run, llama.cpp |
| 230M on CPU, long prompt speed | 56.6 tokens/s | measured | One run, 128 tokens, Q8_0 file |
| 230M on CPU, long prompt first token | 0.414 s | measured | 159-token prompt |
| 230M on CPU, short prompt speed | 58.2 tokens/s | measured | One run, 128 tokens |
| 230M on CPU, short prompt first token | 0.064 s | measured | 14-token prompt |
| 230M on CPU, memory | 562 to 569 MB | measured | Read before and after the runs |
| Accelerator speed advantage | 4.9x | computed | Long prompts, 279.3 / 56.6. Different file format and runtime |
| 4B on accelerator, cold start | 14.26 s | measured | One run |
| 4B on accelerator, long prompt speed | 21.5 tokens/s | measured | One run, 724 tokens |
| 4B on accelerator, long prompt first token | 0.35 s | measured | Timed across a terminal |
| 4B on accelerator, short prompt speed | 24.3 tokens/s | measured | One run, 41 tokens |
| 4B on accelerator, short prompt first token | 0.21 s | measured | Timed across a terminal |
| 4B on accelerator, short prompt total | 1.9 s | measured | Text only, model already loaded |
| Bytes sent by the board over its cable | 8,358,384 | measured | Includes my SSH sessions. Counts bytes, not contents |

Not tested: a real photo. `llima run --help` shows no image option in `cli` mode, and `board_bench_mla.py` sends text only. `--mode web` has not been checked for image input.

## What surprised me

The responses were fast, but the answers weren't always good. I asked if a box in front of a gate was worth an alert. It said yes, and its reason was that nobody reporting a problem suggests the camera may be broken. That reason doesn't follow.

It was honest about the news. I expected it to fail that question, and it said it couldn't know.

The accelerator was 4.9x faster than the CPU on the long prompt, close to my 5x guess. The CPU loaded slightly faster.

## What I'd tell a customer

On-device is the right call mainly for privacy and a lack of internet. If it's confidential data or video that needs to stay on the device, or the internet isn't strong, the model can keep working locally. I assume most functions would run on the model itself, but I haven't tested that. I also haven't compared it with a cloud model on speed.

A fast model might give you useful output, but it could also give you garbage. A model needs to be accurate and fast to be useful.

LFM3 and d1 can't run on this accelerator because no compiled version exists, so on this board they run on the CPU. I didn't run either of them in this lab.

## What this doesn't show

- How long a real photo takes. The tests used text only.
- Whether any model is accurate at this job. Six chat questions are not a test.
- Power or energy use.
- Repeat runs. Most numbers come from one run.

## Problems and fixes

- `Ctrl-C` didn't exit `llima` in an interactive session. I closed the SSH connection and confirmed nothing was still running before measuring.
- `llima run` has no image option in `cli` mode, so the photo test didn't happen.

## Buyer, budget owner, pricing, and what would kill it

Whoever approves the budget for the site, which may be the operations director. I assume it's part of the tech budget. My first price was $25 per site per month. That was a guess, and I compared it with Starlink, which was the wrong comparison because the dish stays in the design. It stays as a placeholder until I know how many incidents a site has each year.

The bet dies if most sites already have enough power and a good link, or if a photo check takes longer than 60 seconds.

## The bet: keep, change or kill, and why

Keep for now. I need more information before I change it, specifically what happens when a photo goes through the model. I cut the model's written reason from the alert, because the one reason I tested didn't follow. Details are in [BET.md](../BET.md).

