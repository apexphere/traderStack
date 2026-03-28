# Architecture

This document explains **why** traderStack is built the way it is.

## The core idea

traderStack is a methodology layer on top of OpenQuant. It turns Claude Code
into an adversarial quant trading mentor using SKILL.md files that call
OpenQuant's CLI (`jesse backtest`, `jesse results`, `jesse optimize`).

The key insight: traders don't need more backtesting tools — OpenQuant already
handles that. They need an AI that pushes back on bad ideas, catches biases,
and refuses to let them risk money until they've demonstrated understanding.

## Architecture

```
OpenQuant Engine (jesse CLI + PostgreSQL + web dashboard)
─────────────────────────────────────────────────────────
  ↑ calls jesse backtest, jesse results, jesse optimize
  │
traderStack Skills (methodology layer)
─────────────────────────────────────────────────────────
  /trader-help    → reads state, recommends next step
  /market-regime  → runs OpenQuant detectors on recent data
  /strategy-thesis → adversarial Q&A → writes thesis.md + scaffolds strategy
  /backtest       → calls jesse backtest → appends results to thesis
  /strategy-review → reads results → PASS/REVISE/REJECT gate
─────────────────────────────────────────────────────────

State flows through two channels:
  1. OpenQuant DB     — backtest results, trades, metrics (jesse results)
  2. Strategy thesis  — strategies/{Name}/thesis.md (written by skills)

  /strategy-thesis writes thesis.md + scaffolds strategy code
       ↓
  /backtest calls jesse backtest → stores results in DB
       ↓
  /strategy-review reads DB results + thesis → gates
```

## Why this architecture

### Skills as methodology, OpenQuant as tooling
Skills don't implement backtesting, regime detection, or optimization — they
call OpenQuant's CLI. This means:
- No duplicate backtesting engines
- Skills stay focused on process, not computation
- When OpenQuant improves (new detectors, behaviors, metrics), skills benefit automatically

### Thesis doc lives with the strategy
The thesis doc (`strategies/{Name}/thesis.md`) lives alongside the strategy code.
This keeps the "why" next to the "what" — when you revisit a strategy months
later, the reasoning is right there.

### OpenQuant DB as source of truth for metrics
Backtest results live in PostgreSQL, not Markdown files. Skills read from the DB
via `jesse results --json-output`. This means:
- Results are queryable and visualizable in the dashboard
- No parsing Markdown tables for metrics
- Historical results persist across sessions

### Quiz gate as foundation
The quiz gates ALL skills on first use. This prevents the failure mode where
a trader runs through the workflow without understanding what the numbers mean.

### Epistemic humility over confidence
The AI doesn't pretend to verify claims. It admits uncertainty and teaches the
user how to verify themselves.

## Dependencies

| Component | Role |
|-----------|------|
| OpenQuant | Backtesting engine, regime detection, optimization, metrics |
| `jesse` CLI | Interface to OpenQuant (backtest, results, optimize) |
| PostgreSQL | Candle data storage, backtest results |
| Web dashboard | Visual results at http://localhost:9000 |

## Design decisions log

| Decision | Chosen | Rejected | Why |
|----------|--------|----------|-----|
| Backtesting engine | OpenQuant (jesse) | bt library | OpenQuant has regime composition, crypto data, event-driven engine |
| Data source | PostgreSQL 1m candles | yfinance | Crypto-native, no survivorship bias for BTC/ETH |
| AI posture | Adversarial + epistemic humility | Sycophantic | Outside voice caught: "verifiable" is a lie |
| Regime model | OpenQuant detectors (ADX, EMA, ATR) | Manual ADX on SPY | Detectors are built-in, tested, crypto-calibrated |
| Benchmark | B&H mandatory (planned) | None | Must prove strategy beats doing nothing |
| Quiz | Gates all skills | Gates /backtest only | "Building a car before teaching to drive" |
| Thesis storage | strategies/{Name}/thesis.md | ~/.traderstack/strategies/ | Thesis lives with the code it describes |
| Results storage | OpenQuant PostgreSQL | Markdown files | Queryable, persistent, visualizable |
