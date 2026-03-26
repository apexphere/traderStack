"""Momentum strategy template for bt.

Buy stocks with the highest recent returns (top N%).
Rebalance periodically.
"""

import bt
import yfinance as yf


def download_data(tickers: list[str], start: str, end: str):
    """Download adjusted close prices from Yahoo Finance."""
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
    lookback_days: int = 63,  # ~3 months
    top_n: int = 5,
    rebalance_days: int = 21,  # ~monthly
    start: str = "2013-01-01",
    end: str = "2019-12-31",
    name: str = "Momentum",
):
    """Build a Momentum bt strategy.

    Select the top N performers over the lookback period.
    Rebalance every rebalance_days trading days.
    Equal weight across selected assets.
    """
    data = download_data(tickers, start, end)

    strategy = bt.Strategy(
        name,
        [
            bt.algos.RunEveryNPeriods(rebalance_days),
            bt.algos.SelectMomentum(n=top_n, lookback=lookback_days),
            bt.algos.WeighEqually(),
            bt.algos.Rebalance(),
        ],
    )

    return bt.Backtest(strategy, data)


def run_and_report(
    tickers: list[str],
    lookback_days: int = 63,
    top_n: int = 5,
    rebalance_days: int = 21,
    start: str = "2013-01-01",
    end: str = "2019-12-31",
    name: str = "Momentum",
) -> dict:
    """Run the strategy and return structured results."""
    backtest = build_strategy(
        tickers, lookback_days, top_n, rebalance_days, start, end, name
    )
    result = bt.run(backtest)

    stats = result.stats
    return {
        "total_return": float(stats.loc["total_return", name]),
        "sharpe": float(stats.loc["daily_sharpe", name]),
        "max_drawdown": float(stats.loc["max_drawdown", name]),
        "num_trades": int(result.get_transactions().shape[0]),
        "name": name,
        "period": f"{start} to {end}",
    }
