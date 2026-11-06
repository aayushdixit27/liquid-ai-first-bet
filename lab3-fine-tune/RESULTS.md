# Lab 3: Fine-tune

Built with Claude to prepare for my Liquid AI product interview. I ran this lab from my phone: I made the calls, and Claude ran the commands on the Mac and the board.

## What I wanted to know

When is fine-tuning worth paying for, and how would I know it learned and didn't just memorize?

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
| Base, 10 new replies | 4/10 | 4 | 2 | measured | Mac. Claude wrote the rows, knowing the model's failures |
| Fine-tuned, 10 new replies | 5/10 | 5 | 0 | measured | Mac. It answered SAFE on all 10, which matches doing nothing |
| Rules then fine-tuned, 10 new replies | 7/10 | 3 | 0 | computed | Rules caught 2 leaks |

My guess before training: 55/60, beating rules. My guess on the 10 new replies: 8/10.

**Lead with the 5/10.** The 56/60 came from rows that share templates with the training data. On a new style, the tuned model caught no leaks. Ten rows is small, but all 5 leaks were missed.

Training: 3.9M of 233.6M weights, 246 training rows, 30 validation rows, about 2.5 minutes on the Mac. The tuned file is 247 MB.

The 32 is not a real improvement. With two examples the model answered SAFE on 59 of 60 rows, so it nearly matched doing nothing.

## What surprised me

The model went from 23/60 to 56/60, close to my 55 guess. Then it caught none of 5 leaks on 10 new replies, against my 8/10 guess.

Two prompt examples swung the model to SAFE on 59 of 60 rows. That scored 32, which looked like a win until I read the answers.

## What I'd tell a customer

Start with the cheapest fix: prompt first, then the harness for anything you can write as exact steps. Fine-tune when the job needs understanding a prompt can't give, and when you have data that looks like production.

Fine-tuning was worth it for patterns like the training data. Beyond that it's unproven, so I'd lead with the lowest score, 5/10. The eval has to include data that doesn't resemble the training set.

Someone has to own the loop: watch for new failures, add them to the eval, decide when to retrain, and check the exact build before it ships.

## What this doesn't show

- A real-world score. Many eval rows share templates with the training data.
- A fair fight with d1. The tuned model trained on this task and d1 did not.
- A clean new-style test. It has only 10 rows, and Claude wrote them knowing the model's failures.
- Accelerator performance. The tuned model ran on the CPU. Compiling for the MLA needs SiMa's Model Compiler, and SiMa recommends a 128 GB machine.

## Buyer, budget owner, pricing, and what would kill it

Pipeline operations or integrity, as a best guess, with $25 per site per month as a placeholder. The kill conditions are in [BET.md](../BET.md).

## The bet: keep, change or kill, and why

Change. Keep the two-tier check and random review, and test the whole system. Both vision models failed the gate claim alone on 254 clean photos, missing 59% and 28% of open gates. Details and the plan are in [BET.md](../BET.md).

