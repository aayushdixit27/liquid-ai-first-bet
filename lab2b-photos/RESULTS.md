# Photo test: can a small vision model see a lasting problem?

Built with Claude to prepare for my Liquid AI product interview. All four runs are done.

## What this has taught me so far

**Accuracy was the problem, and speed wasn't.** Both models checked a photo in about a second or less. Neither model could tell the valve-yard images apart, and Qwen missed all 3 cut fences.

**The wording of the question can break a vision model that can see.** One broad question got PROBLEM on all 49 images from both models. Narrow questions gave Qwen its best score, 36/49. A bigger model made no difference on the broad question.

## What I measured

49 images: 23 problems and 26 normal, so always answering NORMAL would score 26.

| Run | Right | Problems missed | False alarms | Median per photo | Cold start | Label |
|---|---|---|---|---|---|---|
| LFM2.5-VL-450M, broad | 23/49 | 0 | 26 | 118 ms | 5.5 s | measured |
| Qwen3-VL-4B, broad | 23/49 | 0 | 26 | 628 ms | 16.0 s | measured |
| LFM2.5-VL-450M, narrow | 23/49 | 0 | 26 | 211 ms | 6.0 s | measured |
| Qwen3-VL-4B, narrow | 36/49 | 5 | 8 | 931 ms | 16.5 s | measured |

Median times are for one question on broad runs and two on narrow runs.

| Qwen narrow, by group | Right |
|---|---|
| Real gate photos | 30/40 (2 missed, 8 false alarms) |
| Generated box | 3/3 |
| Generated clear | 3/3 |
| Generated cut fence | 0/3 |

Qwen said normal on all 9 generated images, so its 6 right there don't show it can tell them apart. LFM narrow said "Damaged" on 48 images, which set off the code rule. Its gate question alone got 30/40 on real photos, with 20 of 20 closed and 10 of 20 open (computed from the printed answers).

My guesses before running: LFM 35, Qwen 41 on the broad question, cut fences the hardest group. The hardest-group guess was right for Qwen.

## What we did when it failed

1. Every answer was PROBLEM, so we suspected the harness before the model.
2. Claude asked the model about 4 photos in other ways. This was a diagnostic, not a score.
3. On "Is the gate open or closed?" it was right on 3 of 4: closed, open and closed. It said open on `cut-3`, whose gate is closed.
4. On a yes-or-no question it said yes to all 4, so it seems to agree with what it's asked. That cause is my best reading of 4 photos, and isn't proven.
5. Claude added a narrow mode that asks about the gate and the fence separately. A code rule turns the two answers into PROBLEM or NORMAL.

## What this doesn't show

- A clean test of the fix. It was chosen after seeing 4 of these images.
- Accuracy at a valve site. The 40 real photos are from a driveway camera, and the 9 valve-yard images are generated.

## The bet: keep, change or kill, and why

Change. I kept the design and narrowed the job to what the model showed it can see: is the gate open? Cut fences stay unproven until they're tested with closer views, such as cropped sections of the fence. The new claim still needs testing. Details are in [BET.md](../BET.md).

## Sources

See [SOURCES.md](../data/site_photos/SOURCES.md).
