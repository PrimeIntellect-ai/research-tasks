# test_final_state.py
import csv
import json
import os

def test_output_json_exists():
    assert os.path.isfile("/home/user/output.json"), "Output file /home/user/output.json does not exist."

def test_output_json_correctness():
    # Read CSVs to compute expected results dynamically
    products = {}
    with open("/home/user/data/products.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            products[row["product_id"]] = row["category"]

    regions = {}
    with open("/home/user/data/regions.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            regions[row["region_id"]] = row["country"]

    sales = []
    with open("/home/user/data/sales.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            amount = float(row["amount"])
            if amount >= 50.00:
                sales.append({
                    "category": products[row["product_id"]],
                    "country": regions[row["region_id"]],
                    "amount": amount
                })

    # Aggregate data
    agg = {}
    for sale in sales:
        key = (sale["category"], sale["country"])
        if key not in agg:
            agg[key] = {"total_revenue": 0.0, "transaction_count": 0}
        agg[key]["total_revenue"] += sale["amount"]
        agg[key]["transaction_count"] += 1

    # Format and sort according to the rules
    expected_results = []
    for (cat, country), metrics in agg.items():
        expected_results.append({
            "category": cat,
            "country": country,
            "total_revenue": round(metrics["total_revenue"], 2),
            "transaction_count": metrics["transaction_count"]
        })

    # Sort by total_revenue DESC, then country ASC
    expected_results.sort(key=lambda x: (-x["total_revenue"], x["country"]))

    # Read actual output
    with open("/home/user/output.json", "r") as f:
        try:
            actual_results = json.load(f)
        except json.JSONDecodeError:
            assert False, "Output file /home/user/output.json is not valid JSON."

    assert isinstance(actual_results, list), "Output JSON must be an array of objects."
    assert len(actual_results) == len(expected_results), f"Expected {len(expected_results)} records, found {len(actual_results)}."

    for i, (actual, expected) in enumerate(zip(actual_results, expected_results)):
        assert "category" in actual, f"Record {i} is missing 'category'."
        assert "country" in actual, f"Record {i} is missing 'country'."
        assert "total_revenue" in actual, f"Record {i} is missing 'total_revenue'."
        assert "transaction_count" in actual, f"Record {i} is missing 'transaction_count'."

        assert actual["category"] == expected["category"], f"Record {i} category mismatch: expected {expected['category']}, got {actual['category']}."
        assert actual["country"] == expected["country"], f"Record {i} country mismatch: expected {expected['country']}, got {actual['country']}."

        actual_rev = float(actual["total_revenue"])
        assert abs(actual_rev - expected["total_revenue"]) < 0.01, f"Record {i} total_revenue mismatch: expected {expected['total_revenue']}, got {actual_rev}."

        assert actual["transaction_count"] == expected["transaction_count"], f"Record {i} transaction_count mismatch: expected {expected['transaction_count']}, got {actual['transaction_count']}."