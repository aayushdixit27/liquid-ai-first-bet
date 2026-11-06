# Lab 2: Decide

Built with Claude to prepare for my Liquid AI product interview. I ran it on my own SiMa Modalix board.

## What I wanted to know

What belongs in the model, what belongs in the harness, and when is a decision model the right tool?

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

## Threshold

Rules then d1 scored 57/60 at all three thresholds. Only the mistakes changed.

| Threshold | Leaks missed | Safe blocked | Label |
|---|---|---|---|
| 0.3 | 0 | 3 | measured |
| 0.5 | 1 | 2 | measured |
| 0.7 | 3 | 0 | measured |

I'd start at 0.3, because the cost of a leak is greater than the cost of a real customer having to call support. The final number needs real customer data. At 60 rows I can't claim d1 is calibrated.

## Problems and fixes

- The accelerator build added a letter on 21 of 60 answers, such as `LEAKE` and `SAFED`. The parser rejected them. I changed it to accept those as LEAK and SAFE, and re-ran. The CPU build gave clean answers on all 60.

## What surprised me

The same chat model changed 16 of 60 answers between the CPU and accelerator builds. The totals were 23 and 25, so the score hid it. The accelerator build answered LEAK 42 times against 30.

Both chat builds did worse than always answering SAFE, which would score 31.

Rules then d1 scored 57/60 at every threshold. Only the type of mistake changed, so the score can't pick the threshold.

## What I'd tell a customer

Put a cheap rule first. Block what it flags, and send everything else to the decision model. Anything that could be computed with a step-by-step check goes in the harness, such as reversing the digits. Understanding, such as digit words in Spanish, goes to the model.

A decision model is the wrong tool when a rule already does the job, when you need written output, when you can't wait for it, or when its probabilities don't give much clarity.

To test a customer's fine-tuned model, I'd use 60 or so questions with known right answers, see whether the harness or the model catches each one, and read what happened in the results.

## What this doesn't show

- Anything about photos or pipeline sites. This was bank chatbot text.
- A fair model comparison. d1's prompt spells out what counts as a leak, and the chat prompt doesn't.
- A real-world score. 37 of the 60 rows are written examples.
- That d1 is calibrated. 60 rows is too few, and the middle groups have 4 to 6 rows each.
- Rules timing, or the time for rules then d1 run live. The combined score was computed from saved answers.
- What caused the build differences. The prompt layout and software differed as well as the rounding.

## Buyer, budget owner, pricing, and what would kill it

Pipeline operations or integrity, as a best guess. $25 per site per month stays a placeholder. d1 is listed at $0.02 per million input tokens (vendor), about $0.12 for 43,200 text checks (computed), so saving on cloud fees may not be a reason to stay local for text. The bet dies if most valve sites already have enough power and a good link.

## The bet: keep, change or kill, and why

Keep. I narrowed it to pipeline valve sites and cut utilities for now. Details are in [BET.md](../BET.md).

