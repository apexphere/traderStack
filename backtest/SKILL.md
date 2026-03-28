# /backtest — Run Strategy Against Historical Data

You are a rigorous backtesting engine operator. Your job is to take a strategy,
run it against historical data using OpenQuant's CLI, and interpret the results.

## Prerequisites

The OpenQuant server must be running (`jesse run` on port 9000).
The working directory is the OpenQuant project root.

## Quiz Gate

```bash
[ -f ~/.traderstack/.quiz-done ] && echo "QUIZ_DONE" || echo "QUIZ_NEEDED"
```

If `QUIZ_NEEDED`: Tell the user to run `/strategy-thesis` first (which includes
the quiz). Do not proceed.

## Step 1: Identify the Strategy

List available strategies:

```bash
ls -d strategies/*/
```

Ask the user which strategy to backtest (or use the one they mention).
Read the strategy code to understand what it does:

```bash
cat strategies/{StrategyName}/__init__.py
cat strategies/{StrategyName}/config.yaml 2>/dev/null
```

If the strategy has a `thesis.md`, read it for context:

```bash
cat strategies/{StrategyName}/thesis.md 2>/dev/null
```

## Step 2: Run the Backtest

Run the strategy using the OpenQuant CLI:

```bash
.venv/bin/jesse backtest {StrategyName} \
  --start {start_date} --finish {finish_date} \
  --json-output
```

**Default date ranges** (use the user's if specified, otherwise suggest):
- Full available range: 2025-06-01 to 2026-03-26 (BTC-USDT)
- Sensible default: most recent 6 months

**If the strategy is composite** (uses regime detection), a single backtest
already covers all regimes — the detector classifies each bar and routes to
the appropriate behavior automatically. No need for separate regime runs.

**If the backtest fails:**
1. Surface the raw error with a plain-language explanation
2. Check common issues: server not running, strategy import errors, date range
   outside available data (BTC: 2024-11-01 to 2026-03-26, ETH: 2024-06-01 to 2026-03-12)
3. With 210-candle warmup on daily timeframe, earliest usable start is ~2025-06-01

## Step 3: Retrieve and Present Results

```bash
.venv/bin/jesse results --json-output
```

Pick the most recent session (or the one just created). Get detailed results:

```bash
.venv/bin/jesse results {session-id} --json-output
```

Present results clearly:
- Total return, Sharpe ratio, Sortino ratio, max drawdown
- Win rate, number of trades, profit factor
- If composite: regime breakdown (time in each regime, trades per regime)

## Step 4: Run Bias Checks

Evaluate the results for common biases:

### 4.1 Overfitting Check
If the user wants to validate robustness, run optimize with train/test split:

```bash
.venv/bin/jesse optimize {StrategyName} \
  --training-start 2025-06-01 --training-finish 2025-12-31 \
  --testing-start 2026-01-01 --testing-finish 2026-03-26 \
  --trials 50 --objective sharpe
```

Compare training vs testing Sharpe. If testing Sharpe < 50% of training, likely overfit.

### 4.2 Sample Size
- < 30 trades: FAIL — insufficient for any statistical conclusion
- 30-100 trades: WARN — marginal, results may not be reliable
- 100+ trades: PASS — sufficient for basic significance

### 4.3 Regime Robustness (for composite strategies)
- Check the regime log — is performance concentrated in one regime?
- If >80% of profit comes from one regime, the other behaviors may be dead weight

### 4.4 Zero-Trade Check
- If 0 trades: entry conditions too strict, or warmup insufficient
- Common fix: loosen filters, check that indicator timeframes are in data_routes

**Mandatory warning:**
"These bias checks are heuristic. Backtests on crypto data from 2024-2026 cover
a limited set of market conditions. Forward-test (paper trade) before risking
real capital."

## Step 5: Append Results to Thesis Doc (if it exists)

If the strategy has a `thesis.md`, append backtest results:

```markdown
## Backtest Results
- **Period:** {start} to {finish}
- **Total Return:** X%
- **Sharpe:** X.XX
- **Max Drawdown:** -X%
- **Trades:** N
- **Win Rate:** X%

### Bias Checks
| Check | Result | Notes |
| Overfitting | PASS/WARN/FAIL | ... |
| Sample Size | PASS/WARN/FAIL | ... |
| Regime Robustness | PASS/WARN/FAIL | ... |

### Status: BACKTESTED
### Generated On: {timestamp}
```

## Step 6: Journal Entry

Append to `storage/journal.md`:
- Strategy name, Skill: /backtest
- Outcome: backtested (key metrics)
- What happened: which checks passed/failed
- What the AI caught: any warnings or issues

Tell the user: "Backtest complete. Results stored in OpenQuant DB and visible
at http://localhost:9000. Next step: run `/strategy-review` to evaluate
if this strategy is ready."

## Important Rules

- Use `jesse backtest` — NEVER write standalone Python backtest scripts
- A single composite strategy backtest covers all regimes automatically
- Results are stored in PostgreSQL and visible in the web dashboard
- Always check the server is running before attempting a backtest
- Use `--json-output` when you need to parse results programmatically
