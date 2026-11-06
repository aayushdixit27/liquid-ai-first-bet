# Photo test: can a small vision model see a lasting problem?

Built with Claude to prepare for my Liquid AI product interview. In progress: the Qwen and narrow-question runs are still to come.

## What this has taught me so far

**The wording of the question can break a vision model that can see.** One broad question got PROBLEM on all 49 images. In a small check, narrow questions got different answers on different photos. The model could see the images, so the first fix to try is in the harness: ask narrow questions and let code make the decision.

## What I measured

49 images: 23 problems and 26 normal, so always answering NORMAL would score 26.

| Run | Right | Median per photo | Cold start | Label | Limit |
|---|---|---|---|---|---|
| LFM2.5-VL-450M, broad question | 23/49 | about 120 ms on real gate photos | 5.5 s | measured | It answered PROBLEM every time |

My guesses before running: LFM 35, Qwen 41, cut fences the hardest group.

## What we did when it failed

1. Every answer was PROBLEM, so we suspected the harness before the model.
2. Claude asked the model about 4 photos in other ways. This was a diagnostic, not a score.
3. On "Is the gate open or closed?" it was right on 3 of 4: closed, open and closed. It said open on `cut-3`, whose gate is closed.
4. On a yes-or-no question it said yes to all 4, so it seems to agree with what it's asked. That cause is my best reading of 4 photos, and isn't proven.
5. Claude added a narrow mode that asks about the gate and the fence separately. A code rule turns the two answers into PROBLEM or NORMAL.

## What this doesn't show

- Whether narrow questions work across all 49 images. That run hasn't happened.
- A clean test of the fix. It was chosen after seeing 4 of these images.
- Accuracy at a valve site. The 40 real photos are from a driveway camera, and the 9 valve-yard images are generated.

## Sources

See [SOURCES.md](../data/site_photos/SOURCES.md).
