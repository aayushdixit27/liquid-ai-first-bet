# Run the labs

You need a SiMa.ai Modalix DevKit, a Mac, and [Claude Code](https://claude.com/claude-code).

```
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python -r requirements.txt
brew install llama.cpp
./setup/build-llama-for-board.sh
./setup/copy-to-board.sh
```

Models go in `.cache/models/`. Open Claude Code here and type `/lab1`. It walks you through one step at a time.

The eval uses a fictional bank, customers and account numbers. Not affiliated with Liquid AI, SiMa.ai or my employer.
