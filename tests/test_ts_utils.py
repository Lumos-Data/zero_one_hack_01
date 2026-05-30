import unittest
from lib import ts_utils


class TestDateHelpers(unittest.TestCase):
    def test_month_index_is_monotonic_by_month(self):
        self.assertEqual(
            ts_utils.month_index("2024-02-01") - ts_utils.month_index("2024-01-01"), 1
        )
        self.assertEqual(
            ts_utils.month_index("2024-01-01") - ts_utils.month_index("2023-12-01"), 1
        )

    def test_index_to_month_round_trips(self):
        for d in ["1996-04-01", "2023-11-01", "2026-03-01"]:
            self.assertEqual(ts_utils.index_to_month(ts_utils.month_index(d)), d)


if __name__ == "__main__":
    unittest.main()
