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
