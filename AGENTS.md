# traderStack — AI Quant Trading Mentor

traderStack is a collection of SKILL.md files that give Claude Code structured
roles for learning quant trading. Each skill is a specialist: market analyst,
adversarial thesis mentor, backtesting engine operator, and strategy gatekeeper.

## Available skills

Skills live in `trader/`. Invoke them by name (e.g., `/strategy-thesis`).

| Skill | What it does |
|-------|-------------|
| `/trader-help` | Context-aware navigator. Reads your state, recommends next step. |
| `/market-regime` | Detect current market regime (trending/ranging x up/down). |
| `/strategy-thesis` | Adversarial brainstorming. Forces precise, falsifiable thesis. |
| `/backtest` | Test strategy across 4 regimes with 5 bias checks + B&H benchmark. |
| `/strategy-review` | PASS/REVISE/REJECT gate with explicit thresholds. |

## Setup

```bash
pip install -r trader/requirements.txt
./trader/setup
```

## Key conventions

- Skills are plain SKILL.md files read by Claude Code.
- The shared data contract (Strategy Design Doc) flows through all skills.
- All user data lives at `~/.traderstack/` — local files, no server.
- Quiz gate blocks all skills until basic quant concepts are demonstrated.
- Every strategy is benchmarked against buy-and-hold automatically.
