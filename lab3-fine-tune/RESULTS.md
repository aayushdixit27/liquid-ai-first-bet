# Lab 3: Fine-tune

Built with Claude to prepare for my Liquid AI product interview. In progress. From my phone, I sent the commands and Claude ran them on the Mac.

## What I measured

The same 60 fictional bank replies as Lab 2. Always answering SAFE would score 31.

| Run | Right | Leaks missed | Safe blocked | Label | Limit |
|---|---|---|---|---|---|
| LFM2.5-230M base | 23/60 | 18 | 19 | measured | Board CPU, Lab 2 |
| Base with d1's definition | 25/60 | 11 | 24 | measured | Mac |
| Base with definition and two examples | 32/60 | 28 | 0 | measured | Mac |
| Fine-tuned, LoRA, 80 steps | 56/60 | 3 | 1 | measured | Board CPU. Not an accelerator build |
| Fine-tuned, unseen secrets only | 25/26 | 1 | 0 | measured | Written rows share templates with training |
| Rules | 49/60 | 11 | 0 | measured | Lab 2 |
| d1-2B at 0.5 | 53/60 | 5 | 2 | measured | Lab 2. Prompt defined a leak |
| Rules then d1 at 0.5 | 57/60 | 1 | 2 | measured | Lab 2, computed from saved answers |
| Rules then fine-tuned | 58/60 | not split out | not split out | computed | From saved answers |

My guess before training: 55/60, beating rules.

Training: 3.9M of 233.6M weights, 246 training rows, 30 validation rows, about 2.5 minutes on the Mac. The tuned file is 247 MB.

The 32 is not a real improvement. With two examples the model answered SAFE on 59 of 60 rows, so it nearly matched doing nothing.
