# test_final_state.py

import os
import json
import subprocess
import csv
import pytest

def test_venv_and_pandas_installed():
    """Test that the virtual environment exists and pandas is installed inside it."""
    python_bin = "/home/user/venv/bin/python"
    assert os.path.isfile(python_bin), f"Virtual environment Python binary not found at {python_bin}"

    try:
        result = subprocess.run(
            [python_bin, "-c", "import pandas"],
            check=True,
            capture_output=True,
            text=True
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to import pandas in the virtual environment. Error: {e.stderr}")

def test_aggregated_tax_csv():
    """Test that aggregated_tax.csv exists and contains the correct aggregated data."""
    csv_path = "/home/user/output/aggregated_tax.csv"
    assert os.path.isfile(csv_path), f"Output CSV not found at {csv_path}"

    expected_data = {
        "East": 45.0,
        "North": 25.0,
        "South": 40.0
    }

    actual_data = {}
    with open(csv_path, "r", newline="") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header is not None, "CSV file is empty"
        assert [h.strip() for h in header] == ["region_name", "total_tax"], \
            f"CSV header is incorrect. Expected ['region_name', 'total_tax'], got {header}"

        for row in reader:
            if not row:
                continue
            assert len(row) == 2, f"Row does not have exactly 2 columns: {row}"
            region, tax_str = row[0].strip(), row[1].strip()
            try:
                tax = float(tax_str)
            except ValueError:
                pytest.fail(f"Cannot parse total_tax value '{tax_str}' as float for region '{region}'")
            actual_data[region] = tax

    assert len(actual_data) == len(expected_data), \
        f"Expected {len(expected_data)} regions in output, found {len(actual_data)}"

    for region, expected_tax in expected_data.items():
        assert region in actual_data, f"Region '{region}' missing from output CSV"
        assert abs(actual_data[region] - expected_tax) < 1e-6, \
            f"Incorrect total_tax for {region}. Expected {expected_tax}, got {actual_data[region]}"

def test_experiment_log_json():
    """Test that experiment_log.json exists and contains the correct metrics."""
    json_path = "/home/user/experiment_log.json"
    assert os.path.isfile(json_path), f"Experiment log JSON not found at {json_path}"

    with open(json_path, "r") as f:
        try:
            log_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} is not valid JSON")

    expected_keys = {"total_sales_rows", "valid_joined_rows", "max_tax_region"}
    actual_keys = set(log_data.keys())
    assert actual_keys == expected_keys, \
        f"JSON keys mismatch. Expected {expected_keys}, got {actual_keys}"

    assert log_data["total_sales_rows"] == 5, \
        f"Incorrect total_sales_rows. Expected 5, got {log_data['total_sales_rows']}"
    assert log_data["valid_joined_rows"] == 4, \
        f"Incorrect valid_joined_rows. Expected 4, got {log_data['valid_joined_rows']}"
    assert log_data["max_tax_region"] == "East", \
        f"Incorrect max_tax_region. Expected 'East', got '{log_data['max_tax_region']}'"