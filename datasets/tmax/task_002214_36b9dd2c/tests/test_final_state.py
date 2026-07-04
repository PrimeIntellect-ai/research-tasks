# test_final_state.py
import os
import csv
import pytest

def test_cleaned_products_exists():
    path = "/home/user/cleaned_products.csv"
    assert os.path.exists(path), f"Output file {path} is missing."
    assert os.path.isfile(path), f"{path} is not a file."

def test_cleaned_products_content():
    path = "/home/user/cleaned_products.csv"
    assert os.path.exists(path), f"Output file {path} is missing."

    with open(path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "The CSV file is empty."

    header = rows[0]
    expected_header = ["product_id", "price", "category", "discounted", "price_bucket"]
    assert header == expected_header, f"Expected header {expected_header}, but got {header}."

    # Parse data rows
    data_rows = rows[1:]

    # Expected data
    expected_data = [
        ("A1B2C3D4", 15.5, "electronics", "True", "low"),
        ("C3D4E5F6", 45.0, "other", "False", "medium"),
        ("D4E5F6G7", 120.0, "clothing", "False", "high"),
        ("F6G7H8I9", 20.0, "toys", "False", "medium"),
        ("G7H8I9J0", 19.99, "other", "False", "low"),
        ("H8I9J0K1", 50.0, "home", "True", "high"),
    ]

    assert len(data_rows) == len(expected_data), f"Expected {len(expected_data)} rows, but got {len(data_rows)}."

    for i, (actual, expected) in enumerate(zip(data_rows, expected_data)):
        assert len(actual) == 5, f"Row {i+1} does not have exactly 5 columns."

        # product_id
        assert actual[0] == expected[0], f"Row {i+1}: expected product_id '{expected[0]}', got '{actual[0]}'."

        # price (allow formatting differences like 15.5 vs 15.50)
        try:
            actual_price = float(actual[1])
        except ValueError:
            pytest.fail(f"Row {i+1}: price '{actual[1]}' is not a valid float.")
        assert abs(actual_price - expected[1]) < 1e-5, f"Row {i+1}: expected price {expected[1]}, got {actual_price}."

        # category
        assert actual[2] == expected[2], f"Row {i+1}: expected category '{expected[2]}', got '{actual[2]}'."

        # discounted
        assert actual[3] == expected[3], f"Row {i+1}: expected discounted '{expected[3]}', got '{actual[3]}'."

        # price_bucket
        assert actual[4] == expected[4], f"Row {i+1}: expected price_bucket '{expected[4]}', got '{actual[4]}'."

def test_sorted_order():
    path = "/home/user/cleaned_products.csv"
    assert os.path.exists(path), f"Output file {path} is missing."

    with open(path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)

    if len(rows) <= 1:
        return

    product_ids = [row[0] for row in rows[1:]]
    assert product_ids == sorted(product_ids), "The CSV rows are not sorted by product_id in ascending alphabetical order."