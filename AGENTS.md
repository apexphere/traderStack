# traderStack — Adversarial Quant Trading Mentor

traderStack is a methodology layer on top of OpenQuant. Skills call OpenQuant's
CLI (`jesse backtest`, `jesse results`, `jesse optimize`) and add an adversarial
process: thesis validation, bias detection, and PASS/REVISE/REJECT gating.

## Available skills

| Skill | What it does |
|-------|-------------|
| `/trader-help` | Context-aware navigator. Reads OpenQuant state, recommends next step. |
| `/market-regime` | Detect current regime using OpenQuant's built-in detectors. |
| `/strategy-thesis` | Adversarial brainstorming. Writes thesis.md + scaffolds OpenQuant strategy. |
| `/backtest` | Runs `jesse backtest`, checks biases, appends results to thesis. |
| `/strategy-review` | PASS/REVISE/REJECT gate with crypto-calibrated thresholds. |

## Key conventions

- Skills call OpenQuant CLI commands — they don't implement backtesting or regime detection.
- Thesis docs live at `strategies/{Name}/thesis.md` alongside the strategy code.
- Backtest results live in OpenQuant's PostgreSQL, queried via `jesse results`.
- Quiz gate blocks all skills until basic quant concepts are demonstrated.
- All user learning data lives at `~/.traderstack/` — journal and graveyard.
