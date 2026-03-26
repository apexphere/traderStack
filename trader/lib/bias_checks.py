"""Bias detection checks for /backtest.

Five checks, each returns PASS / WARN / FAIL:
1. Lookahead bias (regex heuristic on strategy code)
2. Survivorship bias (always WARNING — Yahoo Finance limitation)
3. Overfitting (in-sample vs out-of-sample Sharpe comparison)
4. Regime check (performance across bull/bear/sideways)
5. Sample size (minimum 100 trades for statistical significance)
"""

import math
import re
from dataclasses import dataclass


@dataclass(frozen=True)
class BiasCheckResult:
    check_name: str
    result: str  # "PASS", "WARN", or "FAIL"
    notes: str


# --- Lookahead Bias (Heuristic) ---

LOOKAHEAD_PATTERNS = (
    # Positive index on data array (accessing future bars)
    (r"data\[\s*[1-9]\d*\s*\]", "data[N] with positive index (future bar access)"),
    # Negative shift (shifting data backward = looking ahead)
    (r"\.shift\(\s*-\s*\d+", ".shift(-N) (backward shift = future data)"),
    # Forward iloc slice
    (r"\.iloc\[\s*.*\+", ".iloc[...+] (possible forward slice)"),
    # Variable names suggesting future data
    (r"\bfuture_", "variable named 'future_*' (suspicious naming)"),
    (r"\btomorrow", "reference to 'tomorrow' (possible lookahead)"),
    (r"\bnext_day", "reference to 'next_day' (possible lookahead)"),
)


def check_lookahead(code: str) -> BiasCheckResult:
    """Regex-based lint for common lookahead bias patterns.

    Known limitation: heuristic only. Will miss indirect lookahead through
    computed columns or custom functions. Every result includes a warning
    to review code manually.
    """
    findings = []
    for pattern, description in LOOKAHEAD_PATTERNS:
        matches = re.findall(pattern, code)
        if matches:
            findings.append(f"  - {description} ({len(matches)} occurrence(s))")

    manual_warning = (
        "IMPORTANT: Lookahead detection is heuristic-only. "
        "Review your data access code manually for indirect lookahead."
    )

    if findings:
        details = "\n".join(findings)
        return BiasCheckResult(
            check_name="Lookahead Bias",
            result="WARN",
            notes=f"Suspicious patterns found:\n{details}\n\n{manual_warning}",
        )

    return BiasCheckResult(
        check_name="Lookahead Bias",
        result="PASS",
        notes=f"No common lookahead patterns detected. {manual_warning}",
    )


# --- Survivorship Bias ---

def check_survivorship() -> BiasCheckResult:
    """Always returns WARNING — Yahoo Finance excludes delisted tickers.

    This is honest about what's testable. For rigorous testing, upgrade
    to Tiingo or Polygon.io which include delisted securities.
    """
    return BiasCheckResult(
        check_name="Survivorship Bias",
        result="WARN",
        notes=(
            "WARNING: Yahoo Finance data excludes delisted stocks. Your "
            "universe may have survivorship bias because only currently "
            "listed stocks are included. Manually verify that your "
            "strategy doesn't rely on knowing which stocks survived.\n\n"
            "For survivorship-bias-free testing, consider upgrading to "
            "Tiingo or Polygon.io data sources."
        ),
    )


# --- Overfitting ---

def check_overfitting(
    in_sample_sharpe: float,
    out_of_sample_sharpe: float,
) -> BiasCheckResult:
    """Compare in-sample vs out-of-sample Sharpe ratios.

    If OOS Sharpe < 50% of IS Sharpe, likely overfit.
    """
    if math.isnan(in_sample_sharpe) or math.isnan(out_of_sample_sharpe):
        return BiasCheckResult(
            check_name="Overfitting",
            result="WARN",
            notes="Cannot compute: Sharpe ratio is NaN (likely zero std deviation).",
        )

    if in_sample_sharpe == 0:
        return BiasCheckResult(
            check_name="Overfitting",
            result="WARN",
            notes="In-sample Sharpe is zero — overfitting check inconclusive.",
        )

    ratio = out_of_sample_sharpe / in_sample_sharpe

    if ratio < 0.5:
        return BiasCheckResult(
            check_name="Overfitting",
            result="WARN",
            notes=(
                f"Likely overfit. Out-of-sample Sharpe ({out_of_sample_sharpe:.2f}) "
                f"is only {ratio:.0%} of in-sample Sharpe "
                f"({in_sample_sharpe:.2f}). A large gap between IS and OOS "
                f"performance suggests the strategy is fitted to historical noise."
            ),
        )

    return BiasCheckResult(
        check_name="Overfitting",
        result="PASS",
        notes=(
            f"OOS Sharpe ({out_of_sample_sharpe:.2f}) is {ratio:.0%} of "
            f"IS Sharpe ({in_sample_sharpe:.2f}). Reasonable consistency."
        ),
    )


# --- Regime Check ---

@dataclass(frozen=True)
class RegimePerformance:
    regime: str
    total_return: float


def check_regime(results: tuple[RegimePerformance, ...]) -> BiasCheckResult:
    """Check if strategy performs across different market regimes.

    Must be positive in at least 2 of 3 regimes.
    """
    if len(results) < 2:
        return BiasCheckResult(
            check_name="Regime Robustness",
            result="WARN",
            notes=f"Only {len(results)} regime(s) tested. Need at least 3 for meaningful check.",
        )

    positive_count = sum(1 for r in results if r.total_return > 0)
    negative_regimes = [r.regime for r in results if r.total_return <= 0]

    if positive_count >= 2:
        if negative_regimes:
            return BiasCheckResult(
                check_name="Regime Robustness",
                result="PASS",
                notes=(
                    f"Positive in {positive_count}/{len(results)} regimes. "
                    f"Underperforms in: {', '.join(negative_regimes)}."
                ),
            )
        return BiasCheckResult(
            check_name="Regime Robustness",
            result="PASS",
            notes=f"Positive across all {len(results)} tested regimes.",
        )

    return BiasCheckResult(
        check_name="Regime Robustness",
        result="FAIL" if positive_count == 0 else "WARN",
        notes=(
            f"Positive in only {positive_count}/{len(results)} regimes. "
            f"Fails in: {', '.join(negative_regimes)}. "
            f"Strategy may be regime-dependent."
        ),
    )


# --- Sample Size ---

def check_sample_size(num_trades: int) -> BiasCheckResult:
    """Check if there are enough trades for statistical significance."""
    if num_trades >= 100:
        return BiasCheckResult(
            check_name="Sample Size",
            result="PASS",
            notes=f"{num_trades} trades — sufficient for statistical significance.",
        )

    if num_trades >= 30:
        return BiasCheckResult(
            check_name="Sample Size",
            result="WARN",
            notes=(
                f"{num_trades} trades — marginal sample size. Results may not "
                f"be statistically reliable. Consider a longer backtest period "
                f"or more frequent trading signals."
            ),
        )

    return BiasCheckResult(
        check_name="Sample Size",
        result="FAIL",
        notes=(
            f"{num_trades} trades — insufficient for any statistical conclusion. "
            f"Minimum 100 trades recommended, 30 is the absolute floor."
        ),
    )
