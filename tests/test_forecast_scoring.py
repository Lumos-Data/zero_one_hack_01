import unittest
from lib import forecast_scoring as fs
from lib import ts_utils as tu


class TestSeasonalNaive(unittest.TestCase):
    def test_naive_mae_lag(self):
        series = {"2020-01-01": 10.0, "2020-02-01": 12.0,
                  "2020-03-01": 11.0, "2020-04-01": 15.0}
        # lag-2 diffs: |11-10|=1, |15-12|=3 -> mean 2.0
        self.assertAlmostEqual(fs.seasonal_naive_mae(series, season=2), 2.0)

    def test_naive_rmse_lag(self):
        series = {"2020-01-01": 10.0, "2020-02-01": 12.0,
                  "2020-03-01": 11.0, "2020-04-01": 15.0}
        # sqrt((1 + 9)/2) = sqrt(5)
        self.assertAlmostEqual(fs.seasonal_naive_rmse(series, season=2), 5.0 ** 0.5)

    def test_naive_too_short_raises(self):
        with self.assertRaises(ValueError):
            fs.seasonal_naive_mae({"2020-01-01": 1.0}, season=2)
