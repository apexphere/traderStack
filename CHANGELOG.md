# Changelog

## [1.0.0] - 2026-03-27

### traderStack v1 — initial release

First release of traderStack, an AI-powered quant trading mentor built on Claude Code.

**5 skills:**
- `/trader-help` — Context-aware navigator that reads your state and tells you what to do next
- `/market-regime` — 2-axis regime detection (trending/ranging x up/down) using ADX and SMA
- `/strategy-thesis` — Adversarial brainstorming that forces precise, falsifiable theses
- `/backtest` — Tests strategies across 4 market regimes with 5 bias checks and automatic B&H benchmark
- `/strategy-review` — PASS/REVISE/REJECT gate with explicit thresholds. Must beat buy-and-hold.

**Infrastructure:**
- Shared Strategy Design Doc data contract connecting all skills
- Quiz gate (5 quant concept questions) gates all skills on first use
- Strategy journal auto-logs every thesis/backtest/review cycle
- Strategy graveyard generates post-mortems for rejected strategies
- 3 strategy archetype templates: momentum, mean reversion, MA crossover
- 55 tests covering data contract, quiz gate, and all 5 bias checks

**Key design decisions:**
- bt library over Backtrader/vectorbt (both unmaintained in free versions)
- Epistemic humility: AI admits uncertainty and teaches verification
- Buy-and-hold benchmark is mandatory — every strategy compared to doing nothing
- 4-quadrant regime model (ADX trending/ranging x SMA up/down)
- Constrained code generation from archetype templates, not free-form

Forked from [gstack](https://github.com/garrytan/gstack) by Garry Tan.
