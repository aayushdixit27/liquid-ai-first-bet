# Lab 3: Fine-tune

Built with Claude to prepare for my Liquid AI product interview. In progress. From my phone, I sent the commands and Claude ran them on the Mac.

## What I measured

The same 60 fictional bank replies as Lab 2. Always answering SAFE would score 31.

| Run | Right | Leaks missed | Safe blocked | Label | Limit |
|---|---|---|---|---|---|
| LFM2.5-230M base | 23/60 | 18 | 19 | measured | Board CPU, Lab 2 |
| Base with d1's definition | 25/60 | 11 | 24 | measured | Mac |
| Base with definition and two examples | 32/60 | 28 | 0 | measured | Mac |

The 32 is not a real improvement. With two examples the model answered SAFE on 59 of 60 rows, so it nearly matched doing nothing.
