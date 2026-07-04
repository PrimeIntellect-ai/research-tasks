# test_final_state.py
import os
import json
import csv
import pytest

def get_expected_data():
    rates_path = "/home/user/config/exchange_rates.json"
    assert os.path.isfile(rates_path), f"Missing exchange rates file: {rates_path}"

    with open(rates_path, "r") as f:
        rates = json.load(f)

    expected_agg = {}
    for chunk in range(20):
        csv_path = f"/home/user/raw_data/sales_chunk_{chunk}.csv"
        assert os.path.isfile(csv_path), f"Missing raw data file: {csv_path}"
        with open(csv_path, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                cat = row["category"]
                rev = float(row["price"]) * int(row["quantity"]) * rates[row["currency"]]
                qty = int(row["quantity"])
                if cat not in expected_agg:
                    expected_agg[cat] = {"total_revenue_usd": 0.0, "total_items": 0}
                expected_agg[cat]["total_revenue_usd"] += rev
                expected_agg[cat]["total_items"] += qty

    expected_list = []
    for cat, vals in expected_agg.items():
        expected_list.append({
            "category": cat,
            "total_revenue_usd": round(vals["total_revenue_usd"], 2),
            "total_items": vals["total_items"]
        })

    # Sort descending by total_revenue_usd, then ascending by category
    expected_list.sort(key=lambda x: (-x["total_revenue_usd"], x["category"]))
    return expected_list

def test_summary_json():
    json_path = "/home/user/processed/summary.json"
    assert os.path.isfile(json_path), f"File missing: {json_path}"

    with open(json_path, "r") as f:
        try:
            agent_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Invalid JSON in {json_path}")

    expected_data = get_expected_data()

    assert isinstance(agent_data, list), "JSON output should be a list of objects"
    assert len(agent_data) == len(expected_data), f"Expected {len(expected_data)} categories, got {len(agent_data)}"

    for exp, agt in zip(expected_data, agent_data):
        assert agt.get("category") == exp["category"], f"Expected category '{exp['category']}' at this position, got '{agt.get('category')}'"
        assert agt.get("total_items") == exp["total_items"], f"Incorrect total_items for category '{exp['category']}'"

        agt_revenue = agt.get("total_revenue_usd")
        assert agt_revenue is not None, f"Missing total_revenue_usd for category '{exp['category']}'"
        assert abs(agt_revenue - exp["total_revenue_usd"]) <= 0.1, f"Incorrect total_revenue_usd for category '{exp['category']}'. Expected {exp['total_revenue_usd']}, got {agt_revenue}"

def test_summary_parquet():
    parquet_path = "/home/user/processed/summary.parquet"
    assert os.path.isfile(parquet_path), f"File missing: {parquet_path}"

    # Check Parquet magic bytes since third-party libraries are not allowed
    with open(parquet_path, "rb") as f:
        header = f.read(4)
        f.seek(-4, os.SEEK_END)
        footer = f.read(4)

    assert header == b"PAR1", f"Invalid Parquet file header in {parquet_path}"
    assert footer == b"PAR1", f"Invalid Parquet file footer in {parquet_path}"