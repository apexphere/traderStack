# Architecture

This document explains **why** traderStack is built the way it is.

## The core idea

traderStack turns Claude Code into an adversarial quant trading mentor using
SKILL.md files. No server, no database, no accounts — just Markdown skills,
Python libraries, and local files.

The key insight: beginners don't need better backtesting tools. They need an AI
that pushes back on bad ideas, catches biases they can't see, and refuses to let
them risk money until they've demonstrated understanding.

## Architecture

```
Claude Code Session
─────────────────────────────────────────────────────────
  /trader-help    → reads ~/.traderstack/ state
  /market-regime  → yfinance data → ADX + SMA classification
  /strategy-thesis → adversarial Q&A → writes Strategy Design Doc
  /backtest       → reads doc → bt library → appends results
  /strategy-review → reads doc + results → PASS/REVISE/REJECT
─────────────────────────────────────────────────────────

All state flows through the Strategy Design Doc:
  ~/.traderstack/strategies/{name}-{date}.md

  /strategy-thesis writes it
       ↓
  /backtest appends results
       ↓
  /strategy-review reads and gates
```

## Why this architecture

### Local files, not a database
Every artifact is a Markdown file the user can read, edit, and version control.
No lock-in, no migration, no server to keep running. Delete `~/.traderstack/`
and you're back to zero.

### Shared data contract
The Strategy Design Doc is the load-bearing wall. All skills read and write the
same schema. This means:
- Skills are decoupled — each only knows about the doc format
- The doc is human-readable — you can inspect it between steps
- New skills can plug in by reading/writing the same format

### Constrained templates, not free-form code generation
The `/backtest` skill generates code from archetype templates (momentum, mean
reversion, MA crossover) rather than generating arbitrary Python. This:
- Dramatically reduces code generation errors
- Makes the generated code teachable (beginner can read and understand it)
- Limits the attack surface for bias detection (known patterns to check)

### Quiz gate as foundation
The quiz gates ALL skills, not just `/backtest`. This prevents the failure mode
where a beginner runs through the workflow without understanding what the numbers
mean. The quiz teaches — it's not a gatekeep.

### Epistemic humility over confidence
The AI doesn't pretend to verify claims. It admits uncertainty and teaches the
user how to verify themselves. This is more honest and more educational than
fake "confidence calibration."

### Buy-and-hold as mandatory benchmark
Every strategy is automatically compared against simply holding SPY. This is the
most important check — if your strategy can't beat doing nothing, the complexity
isn't worth it.

## Dependencies

| Library | Why |
|---------|-----|
| [bt](https://github.com/pmorissette/bt) | Backtesting engine. Maintained, free, simple API. Chosen over Backtrader (unmaintained) and vectorbt (free version frozen). |
| [ffn](https://github.com/pmorissette/ffn) | Financial metrics (Sharpe, drawdown). Auto-installed with bt. |
| [yfinance](https://github.com/ranaroussi/yfinance) | Market data. Free. Known survivorship bias limitation (documented, not hidden). |

## Design decisions log

| Decision | Chosen | Rejected | Why |
|----------|--------|----------|-----|
| Backtesting lib | bt | Backtrader, vectorbt | Both unmaintained (free versions) |
| AI posture | Adversarial + epistemic humility | Sycophantic, confidence calibration | Outside voice caught: "verifiable" is a lie |
| Regime model | 2-axis (ADX x SMA) | 3-bucket (bull/bear/sideways) | Trending vs ranging are different axes from up vs down |
| Benchmark | B&H mandatory | Correlation-only | Correlation doesn't show if strategy beats doing nothing |
| Quiz | Gates all skills | Gates /backtest only | "Building a car before teaching to drive" |
| Code generation | Constrained templates | Free-form | Reduces errors, makes code teachable |
| Data storage | Local Markdown files | Database, cloud | Maximum simplicity, user owns all data |
