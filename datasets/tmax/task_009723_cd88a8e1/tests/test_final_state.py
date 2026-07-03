# test_final_state.py

import os
import json
import pytest

def get_expected_report():
    """Derive the expected report directly from the source JSONL files."""
    users_file = "/home/user/data/users.jsonl"
    products_file = "/home/user/data/products.jsonl"
    orders_file = "/home/user/data/orders.jsonl"

    users = {}
    with open(users_file, "r") as f:
        for line in f:
            if not line.strip(): continue
            u = json.loads(line)
            users[u["_id"]] = {
                "user_id": u["_id"],
                "name": u["profile"]["name"],
                "email": u["profile"]["email"],
                "total_spent": 0.0,
                "electronics_purchased": set(),
                "has_electronics": False
            }

    products = {}
    with open(products_file, "r") as f:
        for line in f:
            if not line.strip(): continue
            p = json.loads(line)
            products[p["prod_id"]] = p

    with open(orders_file, "r") as f:
        for line in f:
            if not line.strip(): continue
            o = json.loads(line)
            if o.get("status") != "completed":
                continue

            uid = o["u_id"]
            if uid not in users:
                continue

            for item in o.get("items", []):
                pid = item["p_id"]
                qty = item["qty"]
                if pid not in products:
                    continue

                prod = products[pid]
                users[uid]["total_spent"] += prod["details"]["price"] * qty

                if prod["details"]["category"] == "Electronics":
                    users[uid]["has_electronics"] = True
                    users[uid]["electronics_purchased"].add(prod["name"])

    report = []
    for uid, udata in users.items():
        if udata["has_electronics"]:
            report.append({
                "user_id": udata["user_id"],
                "name": udata["name"],
                "email": udata["email"],
                "total_spent": float(udata["total_spent"]),
                "electronics_purchased": sorted(list(udata["electronics_purchased"]))
            })

    # Sort by total_spent descending, then name ascending
    report.sort(key=lambda x: (-x["total_spent"], x["name"]))
    return report

def test_report_exists():
    """Check if the report.json file exists."""
    assert os.path.isfile("/home/user/report.json"), "The file /home/user/report.json does not exist."

def test_report_valid_json():
    """Check if the report.json file contains valid JSON."""
    with open("/home/user/report.json", "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("/home/user/report.json is not valid JSON.")
    assert isinstance(data, list), "The root of /home/user/report.json must be a JSON array."

def test_report_content_and_ordering():
    """Validate that the report matches the expected derived state and ordering."""
    expected = get_expected_report()

    with open("/home/user/report.json", "r") as f:
        actual = json.load(f)

    assert len(actual) == len(expected), f"Expected {len(expected)} users in report, got {len(actual)}."

    for i, (exp, act) in enumerate(zip(expected, actual)):
        assert act.get("user_id") == exp["user_id"], f"Mismatch in user_id at index {i}. Expected {exp['user_id']}, got {act.get('user_id')}."
        assert act.get("name") == exp["name"], f"Mismatch in name at index {i}. Expected {exp['name']}, got {act.get('name')}."
        assert act.get("email") == exp["email"], f"Mismatch in email at index {i}. Expected {exp['email']}, got {act.get('email')}."

        actual_spent = act.get("total_spent")
        assert actual_spent is not None, f"Missing total_spent at index {i}."
        assert isinstance(actual_spent, (int, float)), f"total_spent at index {i} must be a number."
        assert abs(actual_spent - exp["total_spent"]) < 1e-5, f"Mismatch in total_spent at index {i}. Expected {exp['total_spent']}, got {actual_spent}."

        actual_electronics = act.get("electronics_purchased")
        assert actual_electronics is not None, f"Missing electronics_purchased at index {i}."
        assert isinstance(actual_electronics, list), f"electronics_purchased at index {i} must be an array."
        assert actual_electronics == exp["electronics_purchased"], f"Mismatch in electronics_purchased at index {i}. Expected {exp['electronics_purchased']}, got {actual_electronics}."