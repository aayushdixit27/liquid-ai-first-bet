---
name: lab3
description: Guides Aayush through Lab 3, fine-tuning a Liquid model on their Mac and deploying it to the Modalix board. Use on /lab3.
---

# Lab 3: fine-tune

**Interview gap this closes:** "you have fine-tuned a model yourself." Liquid's posting says its core offering is customization and fine-tuning, so this is the most important lab. They should finish knowing the real difference between prompting and fine-tuning. It also forces the keep-or-kill decision on the bet.

All lab commands run from the repo folder, so if you're in its parent, start with `! cd liquid-ai-first-bet`.

Read `LABGUIDE.md` in the repo root first and follow it. Do Lab 2 first; its results are the baseline.

Target: 60 minutes.

## Step 1. The baseline and the cost ladder (5 min)

```
.venv/bin/python lab2-decide/score.py lab2-decide/results.jsonl
```

Find the "chat model" line. That's LFM2.5-230M before any change, and the number to beat.

**Concept: the cost ladder.** Use the cheapest fix that works. Prompt first, then harness, and only then fine-tune, because fine-tuning costs data, time and upkeep. Interviewers listen for this.

## Step 2. Try the cheap fix first (8 min)

Have them write a better prompt: say what counts as a leak, add two examples. Put it in `CHAT_HINT`, then re-run only the chat model.

```
export CHAT_HINT="their extra instructions here"
.venv/bin/python lab3-fine-tune/rerun_chat.py lab2-decide/results.jsonl lab3-fine-tune/prompted.jsonl
.venv/bin/python lab3-fine-tune/compare.py lab2-decide/results.jsonl lab3-fine-tune/prompted.jsonl
```

`rerun_chat.py` runs on the Mac with `.cache/models/LFM2.5-230M-GGUF/LFM2.5-230M-Q8_0.gguf`. Did it help? This is the proof for "you know the difference between prompting and fine-tuning in practice." Then `unset CHAT_HINT`.

## Step 3. Understand what's about to happen (5 min)

**Concepts, in plain words:**

- **Weights:** the numbers that are the model.
- **Fine-tuning:** showing the model examples and nudging those numbers so it gets better at one job.
- **LoRA:** instead of changing all 230 million weights, freeze them and train a small add-on of about 4 million. Faster and cheaper, and the base model stays intact.
- **Loss:** a score of how wrong the model is on training examples. Lower is better.
- **Validation loss:** the same score on examples it didn't train on. If training loss falls and validation loss doesn't, it's memorizing and not learning.

Show them `data/train_pool.jsonl`. It has 276 labelled rows. The 60 eval rows aren't in it, and some eval rows use secrets that never appear in it. Liquid suggests 500 to 5,000 examples, so this is on the small side; say so.

## Step 4. Train (8 min)

```
.venv/bin/python lab3-fine-tune/train.py --out runs/tuned
```

Have them watch the loss. Ask what's happening at each print. Ask what `--steps`, `--lr` and `--rank` do. It took about 3 minutes in testing, so close heavy apps first. In one test run, validation loss got worse between steps 80 and 120, which is why the default is 80. Validation loss is noisy here because it only has 30 rows. Ask why more training could make a model worse.

## Step 5. Package it for the board (4 min)

The model is a folder of PyTorch weights. llama.cpp needs a single GGUF file.

```
./lab3-fine-tune/to_gguf.sh runs/tuned
```

Output: `runs/LFM2.5-230M-tuned-Q8_0.gguf`.

## Step 6. Run it on the board, re-score (17 min)

```
scp runs/LFM2.5-230M-tuned-Q8_0.gguf sima@192.168.1.20:/media/nvme/labs/models/
```

Put the same 60 rows through it:

```
ssh sima@192.168.1.20 'cd /media/nvme/labs/scripts && python3 board_judge.py /media/nvme/labs/llama-server skip /media/nvme/labs/models/LFM2.5-230M-tuned-Q8_0.gguf judge_eval.jsonl tuned.jsonl'
scp sima@192.168.1.20:/media/nvme/labs/scripts/tuned.jsonl lab3-fine-tune/tuned.jsonl
.venv/bin/python lab3-fine-tune/compare.py lab2-decide/results.jsonl lab3-fine-tune/tuned.jsonl
```

If `llama-server` isn't on the board, run it on the Mac and label it Mac.

**Be suspicious of a big jump.** All the real rows share one secret, and the replies are similar, so the model may have memorized rather than learned. `compare.py` prints an honest test: only rows whose secret never appeared in training. That's the number to quote, and the gap between it and the overall score is what to explain. If an interviewer asks "how do you know it didn't just memorize?", this is the answer.

**Then go one level harder (5 min).** Unseen secrets still aren't the full test, because the written rows come from the same templates as the training rows. Have them write 10 new replies in `data/my_rows.jsonl`, in a style the model has never seen, half leaks. Use the same fields as `data/judge_eval.jsonl`, with `"category": "mine"` and `"provenance": "mine"`. Then:

```
.venv/bin/python lab3-fine-tune/rerun_chat.py x lab3-fine-tune/mine_base.jsonl .cache/models/LFM2.5-230M-GGUF/LFM2.5-230M-Q8_0.gguf data/my_rows.jsonl
.venv/bin/python lab3-fine-tune/rerun_chat.py x lab3-fine-tune/mine_tuned.jsonl runs/LFM2.5-230M-tuned-Q8_0.gguf data/my_rows.jsonl
.venv/bin/python lab3-fine-tune/compare.py lab3-fine-tune/mine_base.jsonl lab3-fine-tune/mine_tuned.jsonl
```

Expect this to be the lowest score of the three. It's the number that best predicts what a customer would see, so it's the one to lead with.

Don't keep retraining until the eval score looks good. That would turn these 60 rows into training data. One tuning change at most, and report that you made it.

**Limits to name:** the tuned model runs on the CPU, not the accelerator. Compiling for the MLA needs SiMa's Model Compiler, and SiMa recommends a 128 GB machine, so a real product would need that path. That's a genuine gap in the fine-tune-to-deployment loop.

## Step 7. Decide (18 min)

Fill `lab3-fine-tune/RESULTS.md` using the template in `LABGUIDE.md`, with a row each for base, better prompt, fine-tuned and d1. Then out loud, 60 seconds each:

1. When do you prompt, when do you change the harness, and when do you fine-tune?
2. Which did best here, and was fine-tuning worth it? If d1 or rules still won, say so. That's a stronger answer than a win.
3. Who keeps this model current when the attacks change? That's the loop Liquid says Product owns.

Then finish `BET.md`:

- Keep, change or kill, and what evidence changed their mind.
- Buyer, budget owner, pricing, and how a first customer becomes repeatable.
- **The plan engineers could build:** one page in `BET.md` with what to build first, what to cut, and when to kill it.

Then update the coach, as `LABGUIDE.md` says, and tell them this is what unlocks "I've fine-tuned a model." Have them run `grill lab3`.
