"""Tests for the Strategy Design Doc data contract."""

import pytest

from trader.lib.data_contract import (
    ValidationResult,
    has_backtest_results,
    parse_section,
    strategy_file_path,
    validate_doc,
)


VALID_DOC = """# Strategy: Momentum SPY

## Thesis
Stocks that gained >20% in 3 months continue to outperform.

## Evidence
Jegadeesh & Titman (1993) found momentum persists 3-12 months.

## Premises
1. Momentum exists in large-cap US equities
2. Transaction costs don't erode the premium

## Entry Rules
Buy when 3-month return > 20%.

## Exit Rules
Sell when 3-month return < 0% or after 30 days.

## Universe
S&P 500 constituents.

## Position Sizing
Equal weight, max 10 positions.

## Risk Limits
Max drawdown tolerance: 25%. Max position: 10%.

## Expected Metrics
Target Sharpe: 1.0. Expected win rate: 55%.

## Known Weaknesses
Momentum crashes in regime transitions.

## Status: DRAFT
"""

INCOMPLETE_DOC = """# Strategy: Incomplete

## Thesis
Something vague.

## Status: DRAFT
"""

DOC_WITH_BACKTEST = VALID_DOC + """
## Backtest Results
### Regime Performance
| Regime | Period | Total Return | Sharpe | Max Drawdown | Trades |
| Bull | 2013-2019 | 45% | 1.2 | -15% | 150 |
### Bias Checks
| Check | Result | Notes |
| Lookahead | PASS | No patterns found |
### Generated On: 2026-03-26
### Code Path: ~/.traderstack/strategies/momentum-spy-generated.py
"""


class TestValidateDoc:
    def test_valid_doc_passes(self):
        result = validate_doc(VALID_DOC)
        assert result.valid is True
        assert result.missing_sections == ()

    def test_incomplete_doc_fails(self):
        result = validate_doc(INCOMPLETE_DOC)
        assert result.valid is False
        assert len(result.missing_sections) > 0
        assert "Evidence" in result.missing_sections
        assert "Entry Rules" in result.missing_sections

    def test_empty_doc_fails(self):
        result = validate_doc("")
        assert result.valid is False
        assert len(result.missing_sections) == len(
            ("Thesis", "Evidence", "Premises", "Entry Rules", "Exit Rules",
             "Universe", "Position Sizing", "Risk Limits", "Expected Metrics",
             "Known Weaknesses", "Status")
        )

    def test_invalid_status_warns(self):
        doc = VALID_DOC.replace("## Status: DRAFT", "## Status: YOLO")
        result = validate_doc(doc)
        assert result.valid is True  # missing sections still pass
        assert len(result.warnings) > 0
        assert "YOLO" in result.warnings[0]


class TestHasBacktestResults:
    def test_doc_without_results(self):
        assert has_backtest_results(VALID_DOC) is False

    def test_doc_with_results(self):
        assert has_backtest_results(DOC_WITH_BACKTEST) is True


class TestParseSection:
    def test_parse_existing_section(self):
        thesis = parse_section(VALID_DOC, "Thesis")
        assert "Stocks that gained >20%" in thesis

    def test_parse_missing_section(self):
        result = parse_section(VALID_DOC, "Nonexistent")
        assert result == ""

    def test_parse_multiline_section(self):
        premises = parse_section(VALID_DOC, "Premises")
        assert "1." in premises
        assert "2." in premises


class TestStrategyFilePath:
    def test_slug_generation(self):
        path = strategy_file_path("Momentum SPY", "2026-03-26")
        assert "momentum-spy" in path.name
        assert "2026-03-26" in path.name
        assert path.suffix == ".md"

    def test_special_characters_stripped(self):
        path = strategy_file_path("My Strategy!!! @#$", "2026-01-01")
        assert "!" not in path.name
        assert "@" not in path.name
