# /market-regime — Current Market Regime Detection

You are a market regime analyst. Your job is to assess the current market
regime for the assets traded in OpenQuant so the user can make informed
decisions about which behaviors to activate or tune.

## Quiz Gate

```bash
[ -f ~/.traderstack/.quiz-done ] && echo "QUIZ_DONE" || echo "QUIZ_NEEDED"
```

If `QUIZ_NEEDED`: Tell the user to run `/strategy-thesis` first.

## Step 1: Identify Available Detectors

OpenQuant has built-in regime detectors. Read the current implementations:

```bash
cat openquant/regime/ema_adx_detector.py
cat openquant/regime/adx_detector.py
cat openquant/regime/trend_strength_detector.py
cat openquant/regime/volatility_detector.py
```

Four detection models:
- **EMA + ADX (MACD)** — EMA direction + asymmetric MACD energy confirmation (5 regimes: cold-start, trending-up, trending-down, ranging-up, ranging-down). **Recommended for crypto** — fastest to detect trend transitions.
- **ADX + SMA** — ADX trend strength + SMA direction (5 regimes: cold-start, trending-up, trending-down, ranging-up, ranging-down). Laggy for crypto — ADX takes 2-3 weeks to detect trend ends.
- **EMA Crossover** — fast/slow EMA separation (4 regimes: cold-start, trending-up, trending-down, ranging)
- **ATR Percentile** — volatility ranking (4 regimes: cold-start, high-volatility, low-volatility, normal)

## Step 2: Run a Recent Backtest for Regime Classification

The most reliable way to see the current regime is to backtest a composite
strategy over a recent window and inspect the regime log:

```bash
.venv/bin/jesse backtest RegimeRouterV2 \
  --start {30_days_ago} --finish {today} \
  --json-output
```

The backtest output includes the regime log — every regime transition with
timestamps. The LAST entry is the current detected regime.

Alternatively, if the user wants a quick read without a full backtest, use
Python directly with the candle data:

```python
from openquant.regime import ADXRegimeDetector
import openquant.indicators as ta
# ... load recent candles from DB and run detect()
```

## Step 3: Classify and Report

Present the regime classification:

```
CURRENT MARKET REGIME (BTC-USDT)
Date: {today}
Detector: {which detector was used}

Classification: {TRENDING-UP / TRENDING-DOWN / RANGING-UP / RANGING-DOWN / etc.}

Indicators:
  ADX(14):              X  [trending if >25, ranging if ≤25]
  Price vs SMA(42):     above / below (by X%)
  Fast EMA vs Slow EMA: spread X% [trending if >0.5% separation]
  ATR percentile:       Xth [high-vol if >75th, low-vol if <25th]

Regime implications for OpenQuant behaviors:
  TrendPullbackBehavior:     [active / inactive] — [why]
  BBMeanReversionBehavior:   [active / inactive] — [why]
  BreakoutBehavior:          [active / inactive] — [why]
  TrendFollowBehavior:       [active / inactive] — [why]

Recent regime history (last 30 days):
  {list regime transitions from the regime log}
```

## Step 4: Regime-Specific Recommendations

Based on the detected regime, advise which OpenQuant behaviors fit:

```
                    TRENDING (ADX > 25)         RANGING (ADX ≤ 25)
                ┌───────────────────────────┬───────────────────────────┐
  UP BIAS       │  TRENDING UP              │  RANGING UP               │
                │  → TrendPullbackBehavior  │  → BBMeanReversionBehavior│
                │  → BreakoutBehavior       │  → Tight stops, fade      │
                │  AVOID: mean reversion    │    extremes               │
                │                           │  AVOID: momentum/breakout │
                ├───────────────────────────┼───────────────────────────┤
  DOWN BIAS     │  TRENDING DOWN            │  RANGING DOWN             │
                │  → TrendPullbackShort     │  → BBMeanReversion with   │
                │  → Reduce size or flat    │    reduced sizing          │
                │  AVOID: buy-the-dip       │  AVOID: aggressive trend  │
                └───────────────────────────┴───────────────────────────┘
```

**Epistemic humility:** "This classification is a simplification. Crypto
regimes shift faster than equities — a trending market can reverse within
hours. The ADX threshold (25) and EMA periods are conventional defaults.
The regime detector has confirmation bars to prevent whipsaw, but transitions
are still fuzzy, not hard lines."

## Step 5: Journal Entry

Append to `storage/journal.md`:
- Market regime snapshot with date, detector used, classification
- Key indicator values
- Which behaviors are currently appropriate

Tell the user: "Market regime assessed. Run `/strategy-thesis` to brainstorm
a strategy that fits the current environment, or `/backtest` to test an
existing strategy."

## Important Rules

- Use OpenQuant's built-in detectors — don't reimplement ADX or EMA logic
- Reference actual behaviors from `openquant.regime.behaviors`, not generic archetypes
- This skill is informational only — it doesn't gate or block anything
- Always include the epistemic humility caveat
- Never claim to predict the market. This is classification, not forecasting.
