# test_final_state.py

import os
import json
import ast
import pytest

def test_migrate_py_parameterized():
    script_path = "/home/user/etl/migrate.py"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."

    with open(script_path, 'r') as f:
        content = f.read()

    # The query should not use f-strings or string concatenation for the date filter
    # We can parse the AST to check for calls to execute and ensure they have > 1 argument
    # or just do a simple string check to ensure parameterization markers are used.
    assert "?" in content or ":" in content or "%s" in content, "The SQL query does not appear to use parameterization markers (e.g., '?')."

    # Check that f-strings are not used for the SELECT query
    # A simple heuristic: check if 'f"SELECT' or "f'SELECT" is in the file
    assert "f\"SELECT" not in content and "f'SELECT" not in content, "The script still uses an f-string for the SQL query, which is a SQL injection risk."

def test_output_jsonl_schema_and_content():
    output_path = "/home/user/etl/output.jsonl"
    assert os.path.isfile(output_path), f"The output file {output_path} does not exist."

    with open(output_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 3, f"Expected exactly 3 JSON objects in output.jsonl, found {len(lines)}."

    parsed_docs = []
    for i, line in enumerate(lines):
        try:
            doc = json.loads(line)
            parsed_docs.append(doc)
        except json.JSONDecodeError:
            pytest.fail(f"Line {i+1} in output.jsonl is not valid JSON.")

    # Sort docs by customer_id to make assertions deterministic
    parsed_docs.sort(key=lambda x: x.get("customer_id", 0))

    # Expected data derived from the source.db for 2023-10-01
    expected_customers = [
        {
            "customer_id": 1,
            "name": "Alice",
            "region": "North",
            "orders": [{"order_id": 101, "amount": 50.0}, {"order_id": 102, "amount": 25.5}]
        },
        {
            "customer_id": 2,
            "name": "Bob",
            "region": "South",
            "orders": [{"order_id": 103, "amount": 200.0}]
        },
        {
            "customer_id": 4,
            "name": "Diana",
            "region": "North",
            "orders": [{"order_id": 105, "amount": 75.0}]
        }
    ]

    for i, expected in enumerate(expected_customers):
        actual = parsed_docs[i]
        assert "customer_id" in actual, "Missing 'customer_id' in JSON document."
        assert "name" in actual, "Missing 'name' in JSON document."
        assert "region" in actual, "Missing 'region' in JSON document."
        assert "orders" in actual, "Missing 'orders' in JSON document."

        assert actual["customer_id"] == expected["customer_id"], f"Expected customer_id {expected['customer_id']}, got {actual['customer_id']}."
        assert actual["name"] == expected["name"], f"Expected name {expected['name']}, got {actual['name']}."
        assert actual["region"] == expected["region"], f"Expected region {expected['region']}, got {actual['region']}."

        # Sort orders by order_id to ensure order independence
        actual_orders = sorted(actual["orders"], key=lambda x: x.get("order_id", 0))
        expected_orders = sorted(expected["orders"], key=lambda x: x["order_id"])

        assert len(actual_orders) == len(expected_orders), f"Customer {actual['customer_id']} has incorrect number of orders."

        for act_ord, exp_ord in zip(actual_orders, expected_orders):
            assert act_ord.get("order_id") == exp_ord["order_id"], f"Expected order_id {exp_ord['order_id']}, got {act_ord.get('order_id')}."
            assert float(act_ord.get("amount", 0)) == exp_ord["amount"], f"Expected amount {exp_ord['amount']}, got {act_ord.get('amount')}."

def test_aggregate_script_exists():
    # The instructions allowed Python or Node.js, but specified the name aggregate.py
    # We will check for aggregate.py or aggregate.js to be flexible, but strict to the spec
    script_py = "/home/user/etl/aggregate.py"
    script_js = "/home/user/etl/aggregate.js"
    assert os.path.isfile(script_py) or os.path.isfile(script_js), "The aggregation script (aggregate.py or aggregate.js) does not exist."

def test_revenue_by_region_json():
    revenue_path = "/home/user/etl/revenue_by_region.json"
    assert os.path.isfile(revenue_path), f"The output file {revenue_path} does not exist."

    with open(revenue_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {revenue_path} does not contain valid JSON.")

    assert isinstance(data, dict), "The revenue JSON must be a single JSON object (dictionary)."
    assert len(data) == 2, f"Expected exactly 2 regions in revenue JSON, found {len(data)}."

    assert "North" in data, "Missing 'North' region in revenue JSON."
    assert "South" in data, "Missing 'South' region in revenue JSON."

    assert float(data["North"]) == 150.5, f"Expected North revenue to be 150.5, got {data['North']}."
    assert float(data["South"]) == 200.0, f"Expected South revenue to be 200.0, got {data['South']}."