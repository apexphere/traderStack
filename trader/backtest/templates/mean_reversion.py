"""Mean Reversion strategy template for bt.

Buy when price drops below lower Bollinger Band (oversold).
Sell when price returns to the mean.
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
    window: int = 20,
    num_std: float = 2.0,
    start: str = "2013-01-01",
    end: str = "2019-12-31",
    name: str = "Mean Reversion",
):
    """Build a Mean Reversion bt strategy using Bollinger Bands.

    Buy when price < lower band (SMA - num_std * std).
    Sell when price > SMA (mean reversion complete).
    Equal weight across all assets that trigger.
    """
    data = download_data(tickers, start, end)

    # Signal: price below lower Bollinger Band
    sma = data.rolling(window).mean()
    std = data.rolling(window).std()
    lower_band = sma - num_std * std

    signal = data < lower_band

    strategy = bt.Strategy(
        name,
        [
            bt.algos.SelectWhere(signal),
            bt.algos.WeighEqually(),
            bt.algos.Rebalance(),
        ],
    )

    return bt.Backtest(strategy, data)


def run_and_report(
    tickers: list[str],
    window: int = 20,
    num_std: float = 2.0,
    start: str = "2013-01-01",
    end: str = "2019-12-31",
    name: str = "Mean Reversion",
) -> dict:
    """Run the strategy and return structured results."""
    backtest = build_strategy(tickers, window, num_std, start, end, name)
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
