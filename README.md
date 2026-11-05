# Modalix interview labs

Three one-hour labs I ran to prepare for a Product Manager interview at [Liquid AI](https://www.liquid.ai). The posting asks for hands-on model depth: "you have fine-tuned, trained, or built evals for models yourself." So I did, on an edge AI board on my desk.

The labs were built with Claude. I ran them, made the decisions, and wrote up the results.

| Lab | Question | Results |
|---|---|---|
| 1. [On-device](lab1-on-device/) | When is an on-device model the right tool? | Not run yet |
| 2. [Decide](lab2-decide/) | What belongs in the model, and what in the harness? When is a decision model right? | Not run yet |
| 3. [Fine-tune](lab3-fine-tune/) | When is fine-tuning worth it? | Not run yet |

The labs follow one running bet, in [BET.md](BET.md): a vertical, a buyer and a claim that could be proven wrong, kept, changed or killed as the evidence comes in.

## Run them

You need a SiMa.ai Modalix DevKit, a Mac, and [Claude Code](https://claude.com/claude-code).

```
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python -r requirements.txt
brew install llama.cpp
```

Models go in `.cache/models/`. Open Claude Code here and type `/lab1`. It walks you through one step at a time.

## Limits

The eval set is small, and its bank, customers and account numbers are fictional. Every number is labelled measured or vendor.

Not affiliated with Liquid AI, SiMa.ai or my employer.
