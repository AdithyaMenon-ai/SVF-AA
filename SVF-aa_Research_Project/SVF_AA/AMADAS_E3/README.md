# AMADAS E3 — SVF-AA integration prototype

Separate from E1. Contains AMADAS source plus bundled `svf_aa` package.

## Windows PowerShell

```powershell
cd D:\desktop\SVF_AA\AMADAS_E3
uv sync
Copy-Item .env.example .env
ollama list
uv run python create_dataset.py
uv run python main.py
```

Install and run Ollama with `qwen2.5:7b` beforehand (`ollama pull qwen2.5:7b`).
The existing E1 run is unaffected. Reports/models/plots and per-agent verification JSON are saved under `outputs/`.

## Current verification coverage

E3 stage 1 uses `OutputValidator` and `ConstraintVerifier` on each agent's returned update.
Missing/empty outputs and missing required state keys trigger rejection (not automatic retry).
Evidence and reasoning verifiers are bundled but disabled here because their evidence inputs have not been wired to independent sources.
The `confidence`/`risk` values are heuristic, not calibrated probabilities.

## Caveats

A required key can exist with an invalid value; these checks do not establish semantic correctness.
Verification log generation may occur before a downstream node fails. Compare baseline and E3 using the same model/dataset/settings for meaningful evaluation.
