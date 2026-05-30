# prepare_dataset2.py
"""Build cleaned country-level urea price tables + town geo passthrough from dataset 2."""
import csv
import json
import os
from collections import defaultdict

from lib import ts_utils

ROOT = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(ROOT, "data", "dataset2_ssa_urea_USDperKG.csv")
OUT = os.path.join(ROOT, "data", "processed", "dataset2")

LOW_PRICE_FLOOR = 0.10
MIN_YEARS = 3          # < this -> review
STALE_LATEST_YEAR = 2016  # latest_year < this -> review


def build():
    os.makedirs(OUT, exist_ok=True)
    with open(RAW, newline="") as fh:
        raw_rows = list(csv.DictReader(fh))

    collapsed, collapsed_keys = ts_utils.collapse_duplicate_towns(raw_rows)

    # --- towns geo passthrough (raw, cleaned, not aggregated) ---
    geo_fields = ["ISO", "country", "year", "Town",
                  "longitude", "latitude", "distPort", "price_usd_per_kg_ppp"]
    with open(os.path.join(OUT, "dataset2_towns_geo.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=geo_fields)
        w.writeheader()
        for r in collapsed:
            w.writerow({k: r[k] for k in geo_fields})

    # --- country x year aggregation ---
    by_cy = defaultdict(list)   # (ISO, country, year) -> [price floats]
    low_by_cy = defaultdict(int)
    low_towns = []
    for r in collapsed:
        price = float(r["price_usd_per_kg_ppp"])
        key = (r["ISO"], r["country"], r["year"])
        by_cy[key].append(price)
        if ts_utils.flag_low_price(price, LOW_PRICE_FLOOR):
            low_by_cy[key] += 1
            low_towns.append({"ISO": r["ISO"], "year": r["year"],
                              "Town": r["Town"], "price": price})

    cy_rows = []
    for (iso, country, year), prices in sorted(by_cy.items()):
        low = low_by_cy[(iso, country, year)]
        cy_rows.append({
            "ISO": iso,
            "country": country,
            "year": year,
            "median_price_usd_per_kg_ppp": f"{ts_utils.median(prices):.4f}",
            "mean_price": f"{ts_utils.mean(prices):.4f}",
            "town_count": len(prices),
            "flagged_low_price_town_count": low,
            "data_quality": "review" if (low > 0 or len(prices) < 3) else "ok",
        })

    with open(os.path.join(OUT, "urea_country_year.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=[
            "ISO", "country", "year", "median_price_usd_per_kg_ppp", "mean_price",
            "town_count", "flagged_low_price_town_count", "data_quality"])
        w.writeheader()
        w.writerows(cy_rows)

    # --- country summary (recency-aware) ---
    by_country = defaultdict(list)  # ISO -> list of cy_rows
    for row in cy_rows:
        by_country[row["ISO"]].append(row)

    summary_rows = []
    for iso, rows in sorted(by_country.items()):
        years = sorted(int(r["year"]) for r in rows)
        latest = max(years)
        latest_row = [r for r in rows if int(r["year"]) == latest][0]
        all_year_medians = [float(r["median_price_usd_per_kg_ppp"]) for r in rows]
        summary_rows.append({
            "ISO": iso,
            "country": rows[0]["country"],
            "latest_year": latest,
            "latest_year_price": latest_row["median_price_usd_per_kg_ppp"],
            "mean_price_all_years": f"{ts_utils.mean(all_year_medians):.4f}",
            "years_covered": len(years),
            "data_quality": "review" if (len(years) < MIN_YEARS
                                         or latest < STALE_LATEST_YEAR) else "ok",
        })

    with open(os.path.join(OUT, "urea_country_summary.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=[
            "ISO", "country", "latest_year", "latest_year_price",
            "mean_price_all_years", "years_covered", "data_quality"])
        w.writeheader()
        w.writerows(summary_rows)

    with open(os.path.join(OUT, "data_quality_flags.json"), "w") as fh:
        json.dump({
            "collapsed_duplicate_town_years": [list(k) for k in collapsed_keys],
            "low_price_floor": LOW_PRICE_FLOOR,
            "low_price_towns": low_towns,
        }, fh, indent=2)

    print(f"dataset2: {len(cy_rows)} country-years, {len(summary_rows)} countries -> {OUT}")


if __name__ == "__main__":
    build()
