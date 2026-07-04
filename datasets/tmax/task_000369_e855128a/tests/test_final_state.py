# test_final_state.py

import os
import csv
import pytest

PROCESSED_CSV = "/home/user/processed_cars.csv"
METRICS_TXT = "/home/user/metrics.txt"

def test_processed_cars_exists():
    assert os.path.exists(PROCESSED_CSV), f"Missing output file: {PROCESSED_CSV}"
    assert os.path.isfile(PROCESSED_CSV), f"Path is not a file: {PROCESSED_CSV}"

def test_metrics_txt_exists():
    assert os.path.exists(METRICS_TXT), f"Missing output file: {METRICS_TXT}"
    assert os.path.isfile(METRICS_TXT), f"Path is not a file: {METRICS_TXT}"

def test_processed_cars_structure():
    with open(PROCESSED_CSV, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader, None)
        assert headers is not None, "processed_cars.csv is empty."

        expected_columns = ['make', 'vehicle_age', 'mileage_per_year', 'price']
        assert headers == expected_columns, f"Columns in processed_cars.csv do not match expected. Got {headers}, expected {expected_columns}"

        rows = list(reader)

    assert len(rows) == 300, f"Expected exactly 300 rows in processed_cars.csv, got {len(rows)}"

    make_idx = headers.index('make')
    standard_count = sum(1 for r in rows if r[make_idx] == 'Standard')
    luxury_count = sum(1 for r in rows if r[make_idx] == 'Luxury')

    assert standard_count == 150, f"Expected 150 'Standard' cars, got {standard_count}"
    assert luxury_count == 150, f"Expected 150 'Luxury' cars, got {luxury_count}"

def test_metrics_value():
    with open(PROCESSED_CSV, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader, None)
        price_idx = headers.index('price')
        prices = []
        for row in reader:
            prices.append(float(row[price_idx]))

    expected_mean = round(sum(prices) / len(prices), 2)

    with open(METRICS_TXT, mode='r', encoding='utf-8') as f:
        content = f.read().strip()

    assert content != "", "metrics.txt is empty"

    try:
        written_mean = float(content)
    except ValueError:
        pytest.fail(f"Could not parse a numeric value from metrics.txt. Content: '{content}'")

    assert written_mean == expected_mean, f"Expected mean price {expected_mean} based on processed_cars.csv, but metrics.txt contains {written_mean}"
    assert written_mean == 34559.81, f"Expected metrics.txt to contain exactly 34559.81 based on the random seed, got {written_mean}"