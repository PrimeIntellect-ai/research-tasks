# test_final_state.py
import os
import csv
import json
import math

def test_cleaned_data_exists_and_valid():
    path = "/home/user/cleaned_data.csv"
    assert os.path.isfile(path), f"Missing file: {path}"

    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert len(rows) == 100, f"Expected 100 rows in cleaned_data.csv, found {len(rows)}"

    for i, row in enumerate(rows):
        assert 'feature_A' in row, "Missing column 'feature_A' in cleaned_data.csv"
        assert 'feature_B' in row, "Missing column 'feature_B' in cleaned_data.csv"

        val_A = row['feature_A'].strip()
        assert val_A != "", f"Found missing value in feature_A at row {i+1}"

        try:
            float(val_A)
        except ValueError:
            assert False, f"Non-numeric value in feature_A at row {i+1}: {val_A}"

def test_experiment_log_exists_and_valid():
    path = "/home/user/experiment_log.json"
    assert os.path.isfile(path), f"Missing file: {path}"

    with open(path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, "experiment_log.json is not a valid JSON file"

    assert "imputed_count_A" in data, "Missing key 'imputed_count_A' in experiment_log.json"
    assert data["imputed_count_A"] == 10, f"Expected imputed_count_A to be 10, got {data['imputed_count_A']}"

    assert "cap_value_B" in data, "Missing key 'cap_value_B' in experiment_log.json"
    assert isinstance(data["cap_value_B"], (int, float)), "cap_value_B must be a number"

def test_plot_png_exists_and_valid():
    path = "/home/user/plot.png"
    assert os.path.isfile(path), f"Missing file: {path}"

    # Check for valid PNG magic number
    with open(path, 'rb') as f:
        header = f.read(8)
    assert header == b'\x89PNG\r\n\x1a\n', "plot.png is not a valid PNG image"

def test_feature_b_capped():
    # Verify that feature_B in cleaned_data.csv does not exceed the cap_value_B
    log_path = "/home/user/experiment_log.json"
    data_path = "/home/user/cleaned_data.csv"

    if not os.path.isfile(log_path) or not os.path.isfile(data_path):
        pytest.skip("Missing required files for cap verification")

    with open(log_path, 'r', encoding='utf-8') as f:
        try:
            log_data = json.load(f)
            cap_val = float(log_data.get("cap_value_B", float('inf')))
        except:
            pytest.skip("Invalid experiment_log.json")

    with open(data_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            val_B = float(row['feature_B'])
            # Allow minor floating point differences
            assert val_B <= cap_val + 0.01, f"feature_B at row {i+1} ({val_B}) exceeds cap_value_B ({cap_val})"