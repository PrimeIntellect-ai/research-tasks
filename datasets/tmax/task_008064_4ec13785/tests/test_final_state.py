# test_final_state.py

import os
import json
import csv
import math
import pytest

def compute_expected_results(csv_path):
    products = {}
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            products[row['id']] = {
                'f1': float(row['feature1']),
                'f2': float(row['feature2']),
                'f3': float(row['feature3']),
                'price': float(row['price'])
            }

    underpriced_count = 0
    overpriced_count = 0

    for pid, data in products.items():
        predicted = (2.5 * data['f1']) + (1.2 * data['f2']) - (0.8 * data['f3']) + 15.0
        if data['price'] < predicted - 5.0:
            underpriced_count += 1
        elif data['price'] > predicted + 5.0:
            overpriced_count += 1

    p001_data = products.get('P001')
    closest_id = None
    min_dist = float('inf')

    if p001_data:
        for pid, data in products.items():
            if pid == 'P001':
                continue
            dist = math.sqrt(
                (data['f1'] - p001_data['f1'])**2 +
                (data['f2'] - p001_data['f2'])**2 +
                (data['f3'] - p001_data['f3'])**2
            )
            if dist < min_dist:
                min_dist = dist
                closest_id = pid

    return closest_id, underpriced_count, overpriced_count

def test_analysis_output_exists_and_correct():
    csv_path = "/home/user/data/products.csv"
    output_path = "/home/user/output/analysis.json"

    assert os.path.exists(output_path), f"Output file {output_path} does not exist."

    with open(output_path, 'r', encoding='utf-8') as f:
        try:
            output_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {output_path} is not valid JSON.")

    expected_closest, expected_under, expected_over = compute_expected_results(csv_path)

    assert "P001_closest_id" in output_data, "Missing key 'P001_closest_id' in output JSON."
    assert "underpriced_count" in output_data, "Missing key 'underpriced_count' in output JSON."
    assert "overpriced_count" in output_data, "Missing key 'overpriced_count' in output JSON."

    assert output_data["P001_closest_id"] == expected_closest, \
        f"Expected P001_closest_id to be {expected_closest}, got {output_data['P001_closest_id']}"

    assert output_data["underpriced_count"] == expected_under, \
        f"Expected underpriced_count to be {expected_under}, got {output_data['underpriced_count']}"

    assert output_data["overpriced_count"] == expected_over, \
        f"Expected overpriced_count to be {expected_over}, got {output_data['overpriced_count']}"