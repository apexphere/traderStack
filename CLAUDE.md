# traderStack

Methodology layer on top of OpenQuant. Skills call `jesse` CLI commands — they
don't implement their own backtesting or regime detection.

## Commands

```bash
pip install -r requirements.txt      # install Python dependencies (quiz, journal, graveyard)
python -m pytest test/ -v            # run tests (55 tests, <1s)
./setup                              # symlink skills into Claude Code
```

## Available Skills

- `/trader-help` — Context-aware navigator. Reads OpenQuant state, recommends next step.
- `/market-regime` — Regime detection using OpenQuant's built-in detectors (ADX, EMA, ATR)
- `/strategy-thesis` — Adversarial thesis brainstorming → writes thesis.md + scaffolds strategy
- `/backtest` — Runs `jesse backtest`, interprets results, checks for biases
- `/strategy-review` — PASS/REVISE/REJECT gate with crypto-calibrated thresholds

## How skills use OpenQuant

| Skill | OpenQuant commands used |
|-------|----------------------|
| /backtest | `jesse backtest`, `jesse results`, `jesse optimize` |
| /strategy-review | `jesse results` |
| /market-regime | `jesse backtest` (recent window) or direct detector import |
| /strategy-thesis | Reads `strategies/*/config.yaml`, scaffolds new strategy |
| /trader-help | `jesse results`, reads `strategies/*/thesis.md` |

## Project structure

```
traderStack/
├── setup                    # Symlink skills + install deps
├── requirements.txt         # pytest (bias_checks, quiz, journal libs)
├── trader-help/
│   └── SKILL.md             # Context-aware navigator
├── strategy-thesis/
│   └── SKILL.md             # Adversarial thesis brainstorming
├── backtest/
│   └── SKILL.md             # jesse backtest wrapper + bias checks
├── strategy-review/
│   └── SKILL.md             # PASS/REVISE/REJECT gate
├── market-regime/
│   └── SKILL.md             # Regime detection via OpenQuant
├── lib/                     # Shared Python libraries
│   ├── data_contract.py     # Strategy thesis doc schema
│   ├── bias_checks.py       # Bias detection checks
│   ├── quiz.py              # Quiz gate (5 questions)
│   ├── journal.py           # Learning journal logger
│   └── graveyard.py         # Post-mortem generator
└── test/                    # pytest test suite
```

## User data

```
~/.traderstack/
├── .quiz-done          # Quiz passed marker (delete to retake)
├── graveyard/          # Post-mortems for rejected strategies
└── journal.md          # Learning log (auto-updated by skills)

strategies/{Name}/      # In the OpenQuant project
├── __init__.py         # Strategy code
├── config.yaml         # CompositeStrategy config
└── thesis.md           # Strategy thesis doc (written by /strategy-thesis)
```

## Key design decisions

- **OpenQuant is the engine** — skills call `jesse backtest`, not `bt.run()`
- **Thesis doc lives with strategy code** — `strategies/{Name}/thesis.md`
- **Results live in PostgreSQL** — read via `jesse results --json-output`
- **Epistemic humility** over confidence calibration
- **Quiz gate** — gates ALL skills on first use
- **Crypto-calibrated thresholds** — Sharpe, drawdown, trade count adjusted for crypto volatility
