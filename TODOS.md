# TODOS

## v2 — OpenQuant Integration Gaps

### B&H benchmark comparison (OpenQuant issue)

**What:** `jesse backtest` and `jesse results` should include buy-and-hold comparison for the same asset and period.

**Why:** `/strategy-review` needs "does it beat doing nothing?" Currently no way to compare without manual calculation. This is the single most important sanity check.

**Effort:** S (human: ~2 days / CC: ~2 hours)
**Priority:** P1
**Tracked:** GitHub issue on apexphere/openquant

### Strategy scaffolding CLI (OpenQuant issue)

**What:** `jesse new-strategy MyStrategy --composite` generates directory + boilerplate.

**Why:** `/strategy-thesis` currently scaffolds manually via file writes. A CLI command makes this reliable and keeps the boilerplate in sync with framework changes.

**Effort:** S (human: ~1 day / CC: ~1 hour)
**Priority:** P2
**Tracked:** GitHub issue on apexphere/openquant

### Adversarial review annotations (OpenQuant issue)

**What:** `jesse results` with statistical significance flags — trade count vs Sharpe significance, drawdown duration, regime concentration warnings.

**Why:** `/strategy-review` re-derives these from raw numbers every time. Baking interpretation into the results output makes the review faster and more consistent.

**Effort:** M (human: ~1 week / CC: ~4 hours)
**Priority:** P2
**Tracked:** GitHub issue on apexphere/openquant

## v2 — traderStack Improvements

### Paper trading skill

**What:** `/paper-trade` skill — deploy a PASS strategy to paper trading.

**Why:** The workflow ends at PASS with no path forward. A PASS badge without a next step replicates false confidence with more steps.

**Effort:** M (human: ~1 week / CC: ~4 hours)
**Priority:** P1
**Depends on:** At least 1 strategy passing `/strategy-review`

### Trade retrospective

**What:** `/trade-retro` skill — weekly retrospective on paper trading performance.

**Why:** Tracks whether strategies that passed review actually perform in forward testing.

**Effort:** S (human: ~2 days / CC: ~2 hours)
**Priority:** P2
**Depends on:** Paper trading skill

### Remove bt library dependency

**What:** Remove `backtest/templates/` (momentum.py, mean_reversion.py, ma_crossover.py) and bt/yfinance from requirements.txt.

**Why:** Skills now use OpenQuant for backtesting. The bt templates are dead code.

**Effort:** XS
**Priority:** P2

## v3 — Portfolio Management

### Risk review skill

**What:** `/risk-review` — portfolio-level risk assessment across all active strategies.

**Why:** Individual strategy review isn't enough with multiple strategies. Need correlation between strategies, total portfolio drawdown, concentration risk.

**Effort:** M (human: ~1 week / CC: ~4 hours)
**Priority:** P3
**Depends on:** Multiple validated strategies

### Portfolio construction

**What:** How to size and combine multiple strategies into a portfolio.

**Why:** Having 3 PASS strategies doesn't mean running all 3 at full size. Need Kelly criterion, correlation-aware sizing, risk parity allocation.

**Effort:** L (human: ~2 weeks / CC: ~1 week)
**Priority:** P3
**Depends on:** Risk review skill
