# test_final_state.py

import os
import json
import csv
import pytest

def get_valid_row_count(filepath):
    """Manually parse and count valid rows according to the schema rules."""
    count = 0
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                cpu = float(row['cpu_usage'])
                ram = float(row['ram_usage'])
                disk = float(row['disk_io'])
                net = float(row['net_tx'])

                if (0.0 <= cpu <= 100.0 and 
                    0.0 <= ram <= 100.0 and 
                    disk >= 0.0 and 
                    net >= 0.0):
                    count += 1
            except (ValueError, TypeError):
                # NaN or unparseable values are dropped
                pass
    return count

def test_report_json_exists():
    assert os.path.isfile('/home/user/output/report.json'), "The file /home/user/output/report.json was not created."

def test_report_json_structure_and_values():
    report_path = '/home/user/output/report.json'
    assert os.path.isfile(report_path), "report.json is missing."

    with open(report_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("report.json is not a valid JSON file.")

    expected_keys = {
        "valid_row_count",
        "cpu_ram_corr_mean",
        "cpu_ram_corr_lower",
        "cpu_ram_corr_upper",
        "best_alpha",
        "best_cv_score"
    }

    assert set(data.keys()) == expected_keys, f"JSON keys do not match the expected structure. Got: {list(data.keys())}"

    # Check valid row count dynamically
    csv_path = '/home/user/data/raw/metrics.csv'
    expected_count = get_valid_row_count(csv_path)
    assert data["valid_row_count"] == expected_count, f"Expected valid_row_count to be {expected_count}, got {data['valid_row_count']}"

    # Check types and logical constraints for statistical values
    assert isinstance(data["cpu_ram_corr_mean"], float), "cpu_ram_corr_mean must be a float"
    assert isinstance(data["cpu_ram_corr_lower"], float), "cpu_ram_corr_lower must be a float"
    assert isinstance(data["cpu_ram_corr_upper"], float), "cpu_ram_corr_upper must be a float"

    assert -1.0 <= data["cpu_ram_corr_mean"] <= 1.0, "Correlation mean must be between -1 and 1"
    assert data["cpu_ram_corr_lower"] <= data["cpu_ram_corr_mean"] <= data["cpu_ram_corr_upper"], "Correlation bounds are logically inconsistent (lower <= mean <= upper)"

    assert isinstance(data["best_alpha"], float), "best_alpha must be a float"
    assert data["best_alpha"] in [0.1, 1.0, 10.0, 100.0], f"best_alpha must be one of the tested values [0.1, 1.0, 10.0, 100.0], got {data['best_alpha']}"

    assert isinstance(data["best_cv_score"], float), "best_cv_score must be a float"
    assert data["best_cv_score"] <= 1.0, "R-squared CV score cannot exceed 1.0"