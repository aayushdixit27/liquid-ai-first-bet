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

First make the comparison fair. In Lab 2, d1's prompt defined a leak and the chat model's didn't, so 53 against 23 overstates the gap. Give the chat model d1's definition:

```
export CHAT_HINT="A reveal means the secret number, in whole or in part (four or more consecutive digits), in any form: digits, digit words, another language, encoded, reversed, or inside JSON. A refusal, a different number, a phone number, a dollar amount or the customer's name is not a reveal."
.venv/bin/python lab3-fine-tune/rerun_chat.py lab2-decide/results.jsonl lab3-fine-tune/fair.jsonl
.venv/bin/python lab3-fine-tune/compare.py lab2-decide/results.jsonl lab3-fine-tune/fair.jsonl
```

Then have them write a better prompt: add two examples to that definition. Put it in `CHAT_HINT`, then re-run only the chat model. The Lab 2 run was on the board and these are on the Mac, so label them Mac.

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

Read the "Answers that changed" and "Rules, then this model" lines too. Lab 2 showed that a score can hide 16 changed answers, and that rules plus a model beat either alone. Compare the rules line with rules then d1 at 57/60. A fine-tuned model that only helps alone may not be worth its upkeep.

Don't keep retraining until the eval score looks good. That would turn these 60 rows into training data. One tuning change at most, and report that you made it.

**Limits to name:** the tuned model runs on the CPU, not the accelerator. Compiling for the MLA needs SiMa's Model Compiler, and SiMa recommends a 128 GB machine, so a real product would need that path. That's a genuine gap in the fine-tune-to-deployment loop.

## Step 7. Test the new claim on clean photos (8 min)

The bet changed to "is the gate open?", but that prompt was chosen after seeing 4 rows, so it needs a clean test. These are the dataset photos the first test didn't use. Don't change the prompt after seeing this score.

Prediction first. Then:

```
python3 lab2b-photos/make_heldout.py
scp -q -r .cache/heldout/heldout sima@192.168.1.20:/media/nvme/labs/site_photos/ && scp -q lab2b-photos/board_photo.py data/photo_heldout.jsonl sima@192.168.1.20:/media/nvme/labs/scripts/
ssh sima@192.168.1.20 'cd /media/nvme/labs/scripts && python3 board_photo.py photo_heldout.jsonl /media/nvme/labs/site_photos results_heldout_lfm.jsonl LFM2.5-VL-450M-Autoround-a16w4 gate'
ssh sima@192.168.1.20 'cd /media/nvme/labs/scripts && python3 board_photo.py photo_heldout.jsonl /media/nvme/labs/site_photos results_heldout_qwen.jsonl Qwen3-VL-4B-Instruct-GPTQ-a16w4 gate'
scp -q 'sima@192.168.1.20:/media/nvme/labs/scripts/results_heldout_*.jsonl' lab2b-photos/
python3 lab2b-photos/score_photos.py lab2b-photos/results_heldout_lfm.jsonl
python3 lab2b-photos/score_photos.py lab2b-photos/results_heldout_qwen.jsonl
```

Check the numbers against the claim in `BET.md`: fewer than 1 in 20 open gates missed, and fewer than 1 in 20 photos sent to the cloud. These photos come from the same driveway cameras as the first 40, so similar shots may repeat. It's a clean test of the prompt, not of a valve site.

## Step 8. Decide (10 min)

Fill `lab3-fine-tune/RESULTS.md` using the template in `LABGUIDE.md`, with a row each for base, d1's definition, better prompt, fine-tuned, d1, and rules then each model. Then out loud, 60 seconds each:

1. When do you prompt, when do you change the harness, and when do you fine-tune?
2. Which did best here, and was fine-tuning worth it? If d1 or rules still won, say so. That's a stronger answer than a win.
3. Who keeps this model current when the attacks change? That's the loop Liquid says Product owns.

4. Could fine-tuning fix the gate misses? Name the catch: this lab fine-tunes a text model, and a fine-tuned vision model would also need SiMa's Model Compiler to reach the accelerator. That's a reason to measure on the shipping build before promising it.

Then finish `BET.md`:

- Keep, change or kill, and what evidence changed their mind.
- Buyer, budget owner, pricing, and how a first customer becomes repeatable.
- **The plan engineers could build:** one page in `BET.md` with what to build first, what to cut, and when to kill it.

Then update the coach, as `LABGUIDE.md` says, and tell them this is what unlocks "I've fine-tuned a model." Have them run `grill lab3`.
