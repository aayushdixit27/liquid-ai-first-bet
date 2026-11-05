---
name: lab2
description: Guides Aayush through Lab 2, building an eval that compares rules, a decision model and a chat model on the Modalix board. Use on /lab2.
---

# Lab 2: decide

**Interview gap this closes:** "built evals yourself", "what belongs in the model versus the harness", and "when is a decision model the right tool?" They should finish with a measured answer to each. It also tests the bet in `BET.md`.

Read `LABGUIDE.md` in the repo root first and follow it. Do Lab 1 first; `BET.md` comes from it.

Target: 60 minutes.

The task: a bank chatbot replied to a customer. Did the reply leak the customer's secret account number? It comes from Aayush's own `redteam-lab`. The replies are in `data/judge_eval.jsonl`: 60 rows, a mix of real chatbot replies and written examples, all fictional.

## Step 1. What an eval is (8 min)

**Concept:** an eval is a fixed set of inputs with known right answers, so that a change can be scored instead of argued about. Liquid says it wants people who've built these themselves.

Show them 10 rows, with the `label` field hidden, and have them call each one SAFE or LEAK. Then show the labels. Ask: where did you disagree, and whose label is right? Ask whether a reply containing only the customer's name is a leak. Say that the definition is a product decision, and it moves the score.

## Step 2. Predict (3 min)

Have them write down a guess: out of 60, how many will each of these get right?

- **Rules:** a few lines of code that search for the digits.
- **d1-2B:** Liquid's decision model. It gives a probability and generates no text.
- **LFM2.5-230M:** a tiny chat model, asked to answer SAFE or LEAK.

## Step 3. Run it on the board (10 min)

First check that the files are there, and re-run the copy if not:

```
./setup/copy-to-board.sh
```

Run the eval. d1 runs on the board's CPU, because no accelerator build exists:

```
ssh sima@192.168.1.20 'cd /media/nvme/labs/scripts && python3 board_judge.py /media/nvme/labs/llama-server /media/nvme/labs/models/d1-2B-Q4_K_M.gguf /media/nvme/labs/models/LFM2.5-230M-Q8_0.gguf judge_eval.jsonl results.jsonl'
```

Then bring the results back:

```
scp sima@192.168.1.20:/media/nvme/labs/scripts/results.jsonl lab2-decide/results.jsonl
```

If `llama-server` isn't on the board, run the same script on the Mac using the Homebrew `llama-server` and the Mac paths under `.cache/models/`, and label everything Mac.

## Step 3b. The same model on the accelerator (6 min)

**Concept:** the run above used the CPU. This puts the same 60 rows through `LFM2.5-230M-a16w4`, the same Liquid model compiled for the board's MLA accelerator. Prediction first: same answers, or different?

```
ssh sima@192.168.1.20 'cd /media/nvme/labs/scripts && python3 board_judge_mla.py results.jsonl results_mla.jsonl'
scp sima@192.168.1.20:/media/nvme/labs/scripts/results_mla.jsonl lab2-decide/results_mla.jsonl
.venv/bin/python lab3-fine-tune/compare.py lab2-decide/results.jsonl lab2-decide/results_mla.jsonl
```

Here "before" is the CPU build and "after" is the accelerator build. If the rows are slow, the time is mostly model loading, because each row starts a fresh session. If the output is all UNPARSED, read the RAW text it prints and fix the regex.

**The point:** it's the same model with different quantization. If answers change, that's your own proof of "test the exact artifact you ship", and it's why an eval on one build doesn't transfer to another.

## Step 4. Read the scores (8 min)

```
.venv/bin/python lab2-decide/score.py lab2-decide/results.jsonl
```

Take each line in turn. Compare with their guesses. Don't move on until they can say why each judge failed where it did. Open `results.jsonl` and read a few raw answers. If a judge looks broken, say all LEAK or all UNPARSED, assume the harness is at fault until the raw output says otherwise. Fix it, then re-run.

## Step 5. The threshold is a product decision (9 min)

**Concept:** d1 gives a probability. Something has to decide what counts as a leak. That's the threshold, and it lives in the harness.

```
.venv/bin/python lab2-decide/score.py lab2-decide/results.jsonl 0.3
.venv/bin/python lab2-decide/score.py lab2-decide/results.jsonl 0.7
```

Ask: what does a missed leak cost a bank? What does blocking a real customer cost? Have them pick a threshold and defend it in one sentence.

**Calibration:** look at the table `score.py` prints. If d1 says 0.8, is it really a leak about 80 percent of the time? Sixty rows is too few to prove much, so say that. Note that Liquid's card says to calibrate thresholds on your own data, and that no calibration score was found published. Don't overclaim from this table.

## Step 6. Model versus harness (9 min)

Look at the "rules then d1" line. The cheap check runs first and the model handles what rules can't see.

Ask them, for each failure d1 had:

- Would a code rule fix this? Then it belongs in the harness.
- Is it about understanding, such as digit words in Hindi? Then it belongs in the model.
- Would fine-tuning help? That's what Lab 3 tests.

Then the sharp question: which of these three would you put in front of a customer, and when is a decision model the wrong tool?

## Step 7. Write it down, update the bet (7 min)

Fill `lab2-decide/RESULTS.md` using the template in `LABGUIDE.md`. Then have them answer out loud in 60 seconds:

1. When is a decision model the right tool? When isn't it?
2. What did you move from the model into the harness, and why?
3. How would you design an eval for a customer's fine-tuned model?

Update `BET.md`. Does the evidence support it? What result would have broken it? Update buyer, budget owner and pricing using the real numbers: d1 is listed at $0.02 per million input tokens (vendor), and running it on hardware the customer owns has no per-call fee. Keep, change or kill, and what would they cut?

Then update the coach, as `LABGUIDE.md` says.
