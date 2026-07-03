# test_final_state.py
import os
import json
import csv
import math
import pytest

def test_best_match_exists():
    assert os.path.exists("/home/user/best_match.txt"), "/home/user/best_match.txt does not exist"
    with open("/home/user/best_match.txt", "r") as f:
        content = f.read().strip()
    assert content.isdigit(), "best_match.txt must contain only an integer ID"
    # The best match for the query should be either 2 or 5
    assert int(content) in [2, 5], f"Expected best match ID to be 2 or 5, got {content}"

def test_cleaned_inventory_exists():
    assert os.path.exists("/home/user/cleaned_inventory.jsonl"), "/home/user/cleaned_inventory.jsonl does not exist"

def test_cleaned_inventory_content():
    # Read the original CSV to compute expected values
    raw_data = []
    with open("/home/user/inventory.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            raw_data.append(row)

    # 1. Drop missing dims
    clean_data = []
    for row in raw_data:
        if row['length'] == '' or row['width'] == '' or row['height'] == '':
            continue
        clean_data.append(row)

    # 2. Impute
    prices = [float(r['price']) for r in clean_data if r['price'] != '']
    prices.sort()
    n_prices = len(prices)
    if n_prices % 2 == 0:
        median_price = (prices[n_prices//2 - 1] + prices[n_prices//2]) / 2.0
    else:
        median_price = prices[n_prices//2]

    weights = [float(r['weight']) for r in clean_data if r['weight'] != '']
    mean_weight = sum(weights) / len(weights)

    for row in clean_data:
        row['price'] = float(row['price']) if row['price'] != '' else median_price
        row['weight'] = float(row['weight']) if row['weight'] != '' else mean_weight
        row['length'] = float(row['length'])
        row['width'] = float(row['width'])
        row['height'] = float(row['height'])
        row['id'] = int(row['id'])

    # 3. Features
    densities = []
    for row in clean_data:
        row['volume'] = row['length'] * row['width'] * row['height']
        row['density'] = row['weight'] / row['volume']
        densities.append(row['density'])

    # 4. Outliers
    mean_density = sum(densities) / len(densities)
    variance = sum((d - mean_density) ** 2 for d in densities) / (len(densities) - 1)
    std_density = math.sqrt(variance)

    expected_ids = set()
    for row in clean_data:
        z_score = (row['density'] - mean_density) / std_density
        if abs(z_score) <= 2.0:
            expected_ids.add(row['id'])

    # Read the output JSONL
    output_ids = set()
    output_data = []
    with open("/home/user/cleaned_inventory.jsonl", "r") as f:
        for line in f:
            if line.strip():
                record = json.loads(line)
                output_ids.add(record['id'])
                output_data.append(record)

    assert output_ids == expected_ids, f"Expected IDs {expected_ids} after outlier removal, got {output_ids}"

    # Check a specific record to ensure imputation and feature engineering are correct
    for record in output_data:
        if record['id'] == 4: # Missing price originally
            assert math.isclose(record['price'], median_price, rel_tol=1e-5), f"Expected imputed price {median_price}, got {record['price']}"
        if record['id'] == 5: # Missing weight originally
            assert math.isclose(record['weight'], mean_weight, rel_tol=1e-5), f"Expected imputed weight {mean_weight}, got {record['weight']}"
            assert math.isclose(record['volume'], 8.0 * 3.0 * 10.0, rel_tol=1e-5), "Volume calculation incorrect"
            assert math.isclose(record['density'], mean_weight / 240.0, rel_tol=1e-5), "Density calculation incorrect"