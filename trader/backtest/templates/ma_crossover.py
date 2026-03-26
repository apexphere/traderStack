"""Moving Average Crossover strategy template for bt.

This is a constrained template — not free-form code generation.
Parameters are filled from the Strategy Design Doc.

Usage:
    strategy = build_strategy(
        tickers=["SPY"],
        short_window=20,
        long_window=50,
        start="2013-01-01",
        end="2019-12-31",
    )
    result = bt.run(strategy)
"""

import bt
import yfinance as yf
import ffn


def download_data(tickers: list[str], start: str, end: str):
    """Download adjusted close prices from Yahoo Finance.

    Returns a DataFrame with tickers as columns.
    Warns if >5% of data points are NaN.
    """
    data = yf.download(tickers, start=start, end=end, auto_adjust=True)["Close"]

    if data.empty:
        raise ValueError(f"No data returned for {tickers} between {start} and {end}")

    nan_pct = data.isna().mean()
    for ticker in tickers if isinstance(nan_pct, float) else nan_pct.index:
        pct = nan_pct if isinstance(nan_pct, float) else nan_pct[ticker]
        if pct > 0.05:
            print(f"WARNING: {ticker} has {pct:.1%} missing data points")

    return data.dropna()


def build_strategy(
    tickers: list[str],
    short_window: int = 20,
    long_window: int = 50,
    start: str = "2013-01-01",
    end: str = "2019-12-31",
    name: str = "MA Crossover",
):
    """Build a Moving Average Crossover bt strategy.

    Buy when short MA > long MA (golden cross).
    Sell when short MA < long MA (death cross).
    Equal weight across all tickers in universe.
    """
    data = download_data(tickers, start, end)

    # Signal: short MA > long MA
    short_ma = data.rolling(short_window).mean()
    long_ma = data.rolling(long_window).mean()
    signal = short_ma > long_ma

    strategy = bt.Strategy(
        name,
        [
            bt.algos.SelectWhere(signal),
            bt.algos.WeighEqually(),
            bt.algos.Rebalance(),
        ],
    )

    return bt.Backtest(strategy, data)


def build_benchmark(
    start: str = "2013-01-01",
    end: str = "2019-12-31",
    name: str = "Buy & Hold SPY",
):
    """Build a buy-and-hold SPY benchmark for comparison."""
    data = download_data(["SPY"], start, end)

    strategy = bt.Strategy(
        name,
        [
            bt.algos.RunOnce(),
            bt.algos.SelectAll(),
            bt.algos.WeighEqually(),
            bt.algos.Rebalance(),
        ],
    )

    return bt.Backtest(strategy, data)


def run_and_report(
    tickers: list[str],
    short_window: int = 20,
    long_window: int = 50,
    start: str = "2013-01-01",
    end: str = "2019-12-31",
    name: str = "MA Crossover",
) -> dict:
    """Run the strategy AND buy-and-hold benchmark, return both results.

    Every strategy is automatically compared against B&H SPY over the
    same period. If you can't beat doing nothing, your strategy isn't
    worth the complexity.
    """
    strategy_bt = build_strategy(tickers, short_window, long_window, start, end, name)
    benchmark_bt = build_benchmark(start, end)
    result = bt.run(strategy_bt, benchmark_bt)

    stats = result.stats
    bh_name = "Buy & Hold SPY"
    return {
        "strategy": {
            "total_return": float(stats.loc["total_return", name]),
            "sharpe": float(stats.loc["daily_sharpe", name]),
            "max_drawdown": float(stats.loc["max_drawdown", name]),
            "num_trades": int(result.get_transactions().shape[0]),
        },
        "benchmark": {
            "total_return": float(stats.loc["total_return", bh_name]),
            "sharpe": float(stats.loc["daily_sharpe", bh_name]),
            "max_drawdown": float(stats.loc["max_drawdown", bh_name]),
        },
        "beats_benchmark": (
            float(stats.loc["total_return", name])
            > float(stats.loc["total_return", bh_name])
        ),
        "name": name,
        "period": f"{start} to {end}",
    }
