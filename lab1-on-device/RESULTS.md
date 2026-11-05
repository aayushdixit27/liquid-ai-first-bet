# Lab 1: On-device

Built with Claude to prepare for my Liquid AI product interview. I ran it on my own SiMa Modalix board.

## What I wanted to know

In progress.

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
