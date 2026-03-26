# traderStack

## Commands

```bash
pip install -r requirements.txt      # install Python dependencies
python -m pytest test/ -v            # run tests (55 tests, <1s)
./setup                              # symlink skills into Claude Code
```

## Available Skills

- `/trader-help` — Context-aware navigator. Reads state, recommends next step.
- `/market-regime` — 2-axis regime detection (trending/ranging x up/down)
- `/strategy-thesis` — Adversarial strategy brainstorming with epistemic humility
- `/backtest` — bt library backtesting across 4 regimes with B&H benchmark
- `/strategy-review` — PASS/REVISE/REJECT gate with explicit thresholds

## Project structure

```
traderStack/
├── setup                    # Symlink skills + install deps
├── requirements.txt         # bt, ffn, yfinance, pytest
├── trader-help/
│   └── SKILL.md             # Context-aware navigator
├── strategy-thesis/
│   └── SKILL.md             # Adversarial thesis brainstorming
├── backtest/
│   ├── SKILL.md             # bt integration + bias checks
│   └── templates/           # Strategy archetype templates
│       ├── momentum.py
│       ├── mean_reversion.py
│       └── ma_crossover.py
├── strategy-review/
│   └── SKILL.md             # PASS/REVISE/REJECT gate
├── market-regime/
│   └── SKILL.md             # Regime detection
├── lib/                     # Shared Python libraries
│   ├── data_contract.py     # Strategy Design Doc schema
│   ├── bias_checks.py       # 5 bias detection checks
│   ├── quiz.py              # Quiz gate (5 questions)
│   ├── journal.py           # Learning journal logger
│   └── graveyard.py         # Post-mortem generator
├── test/                    # pytest test suite
│   ├── test_data_contract.py
│   ├── test_quiz.py
│   └── test_bias_checks.py
├── CLAUDE.md                # This file
├── README.md                # Project overview
└── ARCHITECTURE.md          # Design decisions
```

## User data

All user state lives at `~/.traderstack/`:

```
~/.traderstack/
├── .quiz-done          # Quiz passed marker (delete to retake)
├── strategies/         # Strategy design docs + generated code
├── graveyard/          # Post-mortems for rejected strategies
└── journal.md          # Learning log (auto-updated by skills)
```

## Testing

```bash
python -m pytest test/ -v   # run all tests
```

Tests cover: data contract validation (11 tests), quiz gate (18 tests),
bias detection checks (26 tests). All tests are fast (<0.1s) and free.

## Key design decisions

- **bt** library for backtesting (maintained, free, simple API)
- **yfinance** for market data (free, known survivorship bias limitation)
- **Epistemic humility** over confidence calibration — AI admits uncertainty
  and teaches verification rather than pretending to verify
- **B&H benchmark mandatory** — every strategy compared against buy-and-hold
- **Quiz gate** — gates ALL skills on first use, not optional
- **4-quadrant regime model** — trending/ranging (ADX) x up/down (SMA)
- **Constrained templates** — code generated from archetypes, not free-form
