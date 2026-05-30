"""Pure-stdlib scoring for the Sybilion forecast bake-off.

Scores each (fertilizer, variant) cell's backtest hindcast against a lag-12
seasonal-naive baseline, excluding stale windows (forecast_end past the last
real data point). P50 = quantile_forecast["0.50"]. No numpy/pandas/math.
"""
from lib.ts_utils import month_index

SEASON = 12
P50_KEY = "0.50"
BAND_80 = ("0.10", "0.90")
BAND_90 = ("0.05", "0.95")


def _sqrt(x):
    return x ** 0.5


def _ordered_values(series):
    items = sorted(series.items(), key=lambda kv: month_index(kv[0]))
    return [float(v) for _d, v in items]


def seasonal_naive_mae(series, season=SEASON):
    """Mean |y_t - y_{t-season}| over the input history. series: {date: float}."""
    vals = _ordered_values(series)
    diffs = [abs(vals[i] - vals[i - season]) for i in range(season, len(vals))]
    if not diffs:
        raise ValueError("series too short for seasonal naive")
    return sum(diffs) / len(diffs)


def seasonal_naive_rmse(series, season=SEASON):
    """Root-mean-square of seasonal-naive errors over the input history."""
    vals = _ordered_values(series)
    sq = [(vals[i] - vals[i - season]) ** 2 for i in range(season, len(vals))]
    if not sq:
        raise ValueError("series too short for seasonal naive")
    return _sqrt(sum(sq) / len(sq))
