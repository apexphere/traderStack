"""Tests for all 5 bias detection checks."""

import math

import pytest

from lib.bias_checks import (
    RegimePerformance,
    check_lookahead,
    check_overfitting,
    check_regime,
    check_sample_size,
    check_survivorship,
)


class TestLookaheadBias:
    def test_clean_code_passes(self):
        code = """
def strategy(data):
    sma = data['Close'].rolling(20).mean()
    return data['Close'] > sma
"""
        result = check_lookahead(code)
        assert result.result == "PASS"
        assert "heuristic-only" in result.notes

    def test_positive_index_warns(self):
        code = "signal = data[1]  # tomorrow's price"
        result = check_lookahead(code)
        assert result.result == "WARN"
        assert "future bar" in result.notes

    def test_negative_shift_warns(self):
        code = "df['future_ret'] = df['Close'].shift(-1)"
        result = check_lookahead(code)
        assert result.result == "WARN"
        assert ".shift(-N)" in result.notes

    def test_forward_iloc_warns(self):
        code = "df.iloc[i+1]"
        result = check_lookahead(code)
        assert result.result == "WARN"

    def test_future_variable_warns(self):
        code = "future_price = get_next_bar()"
        result = check_lookahead(code)
        assert result.result == "WARN"
        assert "future_" in result.notes

    def test_tomorrow_reference_warns(self):
        code = "tomorrow_close = data.shift(-1)['Close']"
        result = check_lookahead(code)
        assert result.result == "WARN"

    def test_multiple_patterns_all_reported(self):
        code = """
signal = data[1]
future_ret = df.shift(-1)
tomorrow = get_price()
"""
        result = check_lookahead(code)
        assert result.result == "WARN"
        assert result.notes.count("-") >= 3  # at least 3 findings

    def test_always_includes_manual_warning(self):
        result = check_lookahead("clean_code = 42")
        assert "heuristic-only" in result.notes


class TestSurvivorshipBias:
    def test_always_warns(self):
        result = check_survivorship()
        assert result.result == "WARN"
        assert "Yahoo Finance" in result.notes
        assert "delisted" in result.notes

    def test_suggests_alternatives(self):
        result = check_survivorship()
        assert "Tiingo" in result.notes or "Polygon" in result.notes


class TestOverfitting:
    def test_consistent_performance_passes(self):
        result = check_overfitting(1.0, 0.8)
        assert result.result == "PASS"
        assert "80%" in result.notes

    def test_severe_degradation_warns(self):
        result = check_overfitting(2.0, 0.5)
        assert result.result == "WARN"
        assert "overfit" in result.notes.lower()

    def test_equal_performance_passes(self):
        result = check_overfitting(1.0, 1.0)
        assert result.result == "PASS"

    def test_nan_sharpe_warns(self):
        result = check_overfitting(float("nan"), 1.0)
        assert result.result == "WARN"
        assert "NaN" in result.notes

    def test_zero_in_sample_warns(self):
        result = check_overfitting(0.0, 0.5)
        assert result.result == "WARN"
        assert "zero" in result.notes.lower()

    def test_both_nan_warns(self):
        result = check_overfitting(float("nan"), float("nan"))
        assert result.result == "WARN"


class TestRegimeCheck:
    def test_all_positive_passes(self):
        results = (
            RegimePerformance("Bull", 0.25),
            RegimePerformance("Bear", 0.05),
            RegimePerformance("Sideways", 0.10),
        )
        result = check_regime(results)
        assert result.result == "PASS"
        assert "all 3" in result.notes.lower()

    def test_two_positive_passes(self):
        results = (
            RegimePerformance("Bull", 0.30),
            RegimePerformance("Bear", -0.10),
            RegimePerformance("Sideways", 0.05),
        )
        result = check_regime(results)
        assert result.result == "PASS"
        assert "Bear" in result.notes

    def test_one_positive_warns(self):
        results = (
            RegimePerformance("Bull", 0.30),
            RegimePerformance("Bear", -0.20),
            RegimePerformance("Sideways", -0.05),
        )
        result = check_regime(results)
        assert result.result == "WARN"

    def test_all_negative_fails(self):
        results = (
            RegimePerformance("Bull", -0.05),
            RegimePerformance("Bear", -0.20),
            RegimePerformance("Sideways", -0.10),
        )
        result = check_regime(results)
        assert result.result == "FAIL"

    def test_too_few_regimes_warns(self):
        results = (RegimePerformance("Bull", 0.20),)
        result = check_regime(results)
        assert result.result == "WARN"
        assert "at least 3" in result.notes


class TestSampleSize:
    def test_sufficient_trades_passes(self):
        result = check_sample_size(150)
        assert result.result == "PASS"

    def test_exactly_100_passes(self):
        result = check_sample_size(100)
        assert result.result == "PASS"

    def test_marginal_trades_warns(self):
        result = check_sample_size(50)
        assert result.result == "WARN"
        assert "marginal" in result.notes.lower()

    def test_insufficient_trades_fails(self):
        result = check_sample_size(10)
        assert result.result == "FAIL"

    def test_zero_trades_fails(self):
        result = check_sample_size(0)
        assert result.result == "FAIL"

    def test_exactly_30_warns(self):
        result = check_sample_size(30)
        assert result.result == "WARN"
