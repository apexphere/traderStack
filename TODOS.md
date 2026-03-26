# TODOS

## v2 — Paper Trading

### Paper trading integration

**What:** `/paper-trade` skill — deploy a PASS strategy to paper trading via Alpaca or QuantConnect API.

**Why:** The current workflow ends at PASS with no path forward. The outside voice in the CEO review flagged: "a PASS badge without a next step replicates false confidence with more steps."

**Effort:** M (human: ~1 week / CC: ~4 hours)
**Priority:** P1
**Depends on:** At least 1 strategy passing `/strategy-review` through dogfooding

### Trade retrospective

**What:** `/trade-retro` skill — weekly retrospective on paper trading performance.

**Why:** Tracks whether strategies that passed review actually perform in forward testing.

**Effort:** S (human: ~2 days / CC: ~2 hours)
**Priority:** P2
**Depends on:** Paper trading integration

## v2 — Data Quality

### Tiingo/Polygon.io data source

**What:** Add support for data sources that include delisted tickers.

**Why:** Yahoo Finance has survivorship bias baked in. The survivorship bias "check" is currently just a warning because the data source makes it untestable.

**Effort:** S (human: ~2 days / CC: ~2 hours)
**Priority:** P2
**Depends on:** None

## v2 — Strategy Archetypes

### Pairs trading template

**What:** Add a pairs trading archetype to `backtest/templates/`.

**Why:** Pairs trading is a common quant strategy that doesn't fit the current 3 archetypes.

**Effort:** S (human: ~1 day / CC: ~1 hour)
**Priority:** P2
**Depends on:** None

### Breakout template

**What:** Add a breakout archetype to `backtest/templates/`.

**Why:** Breakout strategies work in trending regimes — the 4-quadrant regime model already identifies when they're appropriate.

**Effort:** S (human: ~1 day / CC: ~1 hour)
**Priority:** P2
**Depends on:** None

## v3 — Portfolio Management

### Risk review skill

**What:** `/risk-review` — portfolio-level risk assessment across all active strategies.

**Why:** Individual strategy review isn't enough once you have multiple strategies running. Need to check correlation between strategies, total portfolio drawdown, concentration risk.

**Effort:** M (human: ~1 week / CC: ~4 hours)
**Priority:** P3
**Depends on:** Paper trading + multiple validated strategies

### Portfolio construction

**What:** How to size and combine multiple strategies into a portfolio.

**Why:** Having 3 PASS strategies doesn't mean running all 3 at full size. Need Kelly criterion, correlation-aware sizing, and risk parity allocation.

**Effort:** L (human: ~2 weeks / CC: ~1 week)
**Priority:** P3
**Depends on:** Risk review skill

## Future Ideas

### Community sharing

**What:** Share validated Strategy Design Docs with other traderStack users.

**Why:** The design doc format is standardized — it could become a sharing format. But this is an ocean, not a lake — community features are a different product.

**Priority:** P4

### Live trading

**What:** Deploy strategies with real money via broker API.

**Why:** The ultimate goal. But this needs extensive testing, risk management, regulatory awareness, and should only happen after months of paper trading validation.

**Priority:** P4
**Depends on:** Paper trading proven, risk review, portfolio construction
