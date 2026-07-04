# test_final_state.py

import os
import json
import pytest

def test_cleaned_products_exists():
    filepath = "/home/user/cleaned_products.jsonl"
    assert os.path.exists(filepath), f"File {filepath} does not exist. The C++ program did not generate the expected output file."

def test_cleaned_products_content():
    filepath = "/home/user/cleaned_products.jsonl"
    assert os.path.exists(filepath), "Missing output file."

    with open(filepath, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 5, f"Expected exactly 5 valid records, but found {len(lines)}."

    parsed_records = []
    for i, line in enumerate(lines):
        try:
            record = json.loads(line)
            parsed_records.append(record)
        except json.JSONDecodeError:
            pytest.fail(f"Line {i+1} is not valid JSON: {line}")

    # Check ordering by id
    ids = [r.get("id") for r in parsed_records]
    assert ids == sorted(ids), "The output records are not ordered by 'id' ascending."

    expected_data = {
        "A1": {"name": "Café", "calculated_volume": 100.00, "numeric_price": 12.50},
        "A2": {"name": "抹茶", "calculated_volume": 600.00, "numeric_price": 1500.00},
        "B2": {"name": "سجادة", "calculated_volume": 512.00, "numeric_price": 45.00},
        "C1": {"name": "Crème", "calculated_volume": 60.00, "numeric_price": 15.25},
        "C2": {"name": "Té", "calculated_volume": 2000.00, "numeric_price": 20.00},
    }

    assert len(parsed_records) == len(expected_data), "Incorrect number of records."

    for record in parsed_records:
        rid = record.get("id")
        assert rid in expected_data, f"Unexpected record with id {rid}."

        expected = expected_data[rid]
        assert record.get("name") == expected["name"], f"Incorrect name for id {rid}."

        calc_vol = record.get("calculated_volume")
        assert isinstance(calc_vol, (int, float)), f"calculated_volume for {rid} must be a number."
        assert abs(calc_vol - expected["calculated_volume"]) < 1e-5, f"Incorrect calculated_volume for id {rid}."

        num_price = record.get("numeric_price")
        assert isinstance(num_price, (int, float)), f"numeric_price for {rid} must be a number."
        assert abs(num_price - expected["numeric_price"]) < 1e-5, f"Incorrect numeric_price for id {rid}."

def test_two_decimal_places_formatting():
    filepath = "/home/user/cleaned_products.jsonl"
    assert os.path.exists(filepath), "Missing output file."

    with open(filepath, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    for i, line in enumerate(lines):
        # We check if the expected numeric values are formatted to 2 decimal places in the raw string
        # A simple way is to check that there's a dot followed by exactly two digits before a comma or brace
        import re
        # Find all numbers with decimals in the line
        decimals = re.findall(r'\.\d+', line)
        for dec in decimals:
            assert len(dec) == 3, f"Line {i+1} does not format numbers to exactly 2 decimal places: {line}"