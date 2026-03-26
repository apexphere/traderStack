# traderStack

An AI-powered quant trading mentor built on Claude Code. Inspired by [gstack](https://github.com/garrytan/gstack).

traderStack turns Claude Code into an adversarial trading coach — one that pushes back on your thesis, catches your biases, and won't let you risk money until you've earned it. Built for developers who want to learn quant trading without losing money to rookie mistakes.

**This is not a trading platform.** It's a structured learning workflow with guardrails. The AI is deliberately adversarial — it challenges your ideas, flags your biases, and compares every strategy against buy-and-hold before letting it pass.

## Quick start

```bash
# Clone
git clone https://github.com/apexphere/traderStack.git
cd traderStack

# Install skills + Python dependencies
./setup

# Start a new Claude Code session
/trader-help
```

## The workflow

```
/market-regime → /strategy-thesis → /backtest → /strategy-review
      ↑                                              │
      │              ┌─────── PASS ────→ paper trade (v2)
      │              │
      └── REVISE ←───┤
                     │
                     └─────── REJECT ──→ graveyard + lessons
```

Every strategy goes through the full loop. No shortcuts. No skipping steps.

## Skills

| Skill | Role | What it does |
|-------|------|--------------|
| `/trader-help` | **Navigator** | Reads your `~/.traderstack/` state and tells you exactly where you are and what to do next. Not a static help page — a dynamic assessment of your journey. |
| `/market-regime` | **Market Analyst** | 2-axis regime detection: trending vs ranging (ADX) x up vs down (SMA). Four quadrants with strategy recommendations and what to AVOID in each regime. |
| `/strategy-thesis` | **Adversarial Mentor** | Forces you to articulate a precise, falsifiable thesis. Searches academic evidence. Challenges every premise. Uses epistemic humility — admits when it's uncertain and teaches you how to verify. |
| `/backtest` | **Backtesting Engine** | Tests your strategy across 4 market regimes (bull, bear, sideways, out-of-sample) using the [bt](https://github.com/pmorissette/bt) library. Runs 5 bias checks. **Automatically benchmarks against buy-and-hold.** |
| `/strategy-review` | **Adversarial Gate** | PASS / REVISE / REJECT with explicit thresholds. Checks statistical significance, drawdown, transaction costs, B&H benchmark, SPY correlation, and regime robustness. Optional Codex second opinion on PASS. |

## What makes this different

**The AI pushes back.** Most AI tools are sycophantic — they agree with whatever you say. traderStack's skills are deliberately adversarial. They challenge your thesis, cite counter-evidence, and refuse to validate strategies with known biases.

**Epistemic humility.** When the AI isn't sure, it says so. Every uncertain claim comes with: "I could be wrong. Here's how you'd verify this yourself: [specific search terms, databases, textbook chapters]." It teaches you to verify, not to trust blindly.

**Buy-and-hold is the bar.** Every strategy is automatically compared against simply buying and holding SPY over the same period. If your strategy can't beat doing nothing, it fails the review — no matter how clever it looks.

**Quiz gate.** Before you can use any skill, you pass a 5-question quiz on core quant concepts (lookahead bias, Sharpe ratio, survivorship bias, overfitting, drawdown). This prevents the exact failure mode the tool is designed to prevent: running backtests without understanding what the numbers mean.

**Your failures are your best teacher.** Rejected strategies get auto-generated post-mortems in the graveyard (`~/.traderstack/graveyard/`). Every cycle is logged to your strategy journal (`~/.traderstack/journal.md`). Over time, these become your most valuable assets.

## Infrastructure

| Component | Purpose |
|-----------|---------|
| `lib/data_contract.py` | Strategy Design Doc schema — the shared artifact that flows through all skills |
| `lib/bias_checks.py` | 5 bias detection checks (lookahead, survivorship, overfitting, regime, sample size) |
| `lib/quiz.py` | Quiz gate — 5 questions, gates all skills on first use |
| `lib/journal.py` | Auto-logs every thesis → backtest → review cycle |
| `lib/graveyard.py` | Post-mortem generator for rejected strategies |

## Strategy archetypes (v1)

Three constrained templates for the bt backtesting library:

| Archetype | What it does | Template |
|-----------|-------------|----------|
| **Momentum** | Buy top performers over lookback period | `backtest/templates/momentum.py` |
| **Mean Reversion** | Buy when price drops below Bollinger Band | `backtest/templates/mean_reversion.py` |
| **MA Crossover** | Buy on golden cross (short MA > long MA) | `backtest/templates/ma_crossover.py` |

## Testing

```bash
# Run all tests (55 tests, ~0.05s)
python -m pytest test/ -v
```

Tests cover: data contract validation, quiz gate, and all 5 bias detection checks.

## Data

Everything is local files. No server, no database, no accounts.

```
~/.traderstack/
├── .quiz-done          # Quiz completion marker (delete to retake)
├── strategies/         # Strategy design docs + generated code
├── graveyard/          # Post-mortems on rejected strategies
└── journal.md          # Your learning log (auto-updated)
```

## Dependencies

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) (runtime for skills)
- [bt](https://github.com/pmorissette/bt) (backtesting engine)
- [yfinance](https://github.com/ranaroussi/yfinance) (market data)
- [ffn](https://github.com/pmorissette/ffn) (financial metrics, auto-installed with bt)
- [pytest](https://docs.pytest.org/) (testing)

## Acknowledgments

traderStack is a fork of [gstack](https://github.com/garrytan/gstack) by [Garry Tan](https://x.com/garrytan). The skill architecture, adversarial questioning patterns, review pipeline, and the "Boil the Lake" completeness principle all come from gstack. traderStack adapts that workflow philosophy for quant trading strategy development.

## License

MIT
