# Lab 2: Decide

Built with Claude to prepare for my Liquid AI product interview. I ran it on my own SiMa Modalix board.

## What I measured

60 replies from a fictional bank chatbot: 29 leaks, 31 safe. 23 real chatbot replies, 37 written examples. Always answering SAFE would score 31.

| Judge | Right | Leaks missed | Safe blocked | Median per reply | Label | Limit |
|---|---|---|---|---|---|---|
| Rules | 49/60 | 11 | 0 | not timed | measured | Rules search for digits only |
| d1-2B at 0.5, CPU | 53/60 | 5 | 2 | 5,358 ms | measured | Its prompt spells out what counts as a leak. The chat prompt doesn't |
| LFM2.5-230M, CPU | 23/60 | 18 | 19 | 256 ms | measured | One-line prompt, no rules given |
| LFM2.5-230M, accelerator | 25/60 | 11 | 24 | about 25 ms once loaded | measured | Prompt layout differs slightly from the CPU run |
| Rules then d1 at 0.5 | 57/60 | 1 | 2 | not timed | measured | 60 rows, written partly by hand |

My guesses before running: rules 45, d1 50, chat model 35. After seeing the chat model's score, I changed rules and d1 to 15, which was wrong.

16 of 60 answers changed between the CPU and accelerator builds. I guessed 5.

## Problems and fixes

- The accelerator build added a letter on 21 of 60 answers, such as `LEAKE` and `SAFED`. The parser rejected them. I changed it to accept those as LEAK and SAFE, and re-ran. The CPU build gave clean answers on all 60.
