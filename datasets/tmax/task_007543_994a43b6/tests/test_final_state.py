# test_final_state.py

import os
import json
import csv
import math
import shutil
import pytest

def round_half_up(n):
    """Standard rounding: rounds half up to match typical bash/awk rounding."""
    return math.floor(n + 0.5)

def test_dependencies_installed():
    """Test that datamash and jq are installed."""
    assert shutil.which("datamash") is not None, "datamash is not installed on the system."
    assert shutil.which("jq") is not None, "jq is not installed on the system."

def test_scripts_exist_and_executable():
    """Test that detect.sh and sweep.sh exist and are executable."""
    detect_path = "/home/user/pipeline/detect.sh"
    sweep_path = "/home/user/pipeline/sweep.sh"

    assert os.path.isfile(detect_path), f"{detect_path} is missing."
    assert os.access(detect_path, os.X_OK), f"{detect_path} is not executable."

    assert os.path.isfile(sweep_path), f"{sweep_path} is missing."
    assert os.access(sweep_path, os.X_OK), f"{sweep_path} is not executable."

def test_experiments_json_correctness():
    """Test that experiments.json contains the correct dynamically computed results."""
    json_path = "/home/user/pipeline/experiments.json"
    assert os.path.isfile(json_path), f"{json_path} is missing."

    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{json_path} does not contain valid JSON.")

    assert isinstance(data, list), "experiments.json should contain a JSON array."
    assert len(data) == 5, f"experiments.json should contain exactly 5 results, found {len(data)}."

    # Compute expected anomalies from the actual CSV
    csv_path = "/home/user/pipeline/sensor_data.csv"
    assert os.path.isfile(csv_path), f"{csv_path} is missing."

    values = []
    missing_count = 0
    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            val = row["value"].strip()
            if val == "":
                missing_count += 1
            else:
                values.append(float(val))

    if not values:
        pytest.fail("No valid data found in CSV to compute truth.")

    # 1. Calculate true mean of the value column, ignoring empty rows, rounded to nearest int
    mean = sum(values) / len(values)
    rounded_mean = round_half_up(mean)

    # 2. Impute missing values with the rounded mean
    imputed_values = values + [rounded_mean] * missing_count

    # 3. Calculate Mean Absolute Deviation (MAD), rounded to nearest int
    deviations = [abs(v - rounded_mean) for v in imputed_values]
    mad = sum(deviations) / len(imputed_values)
    rounded_mad = round_half_up(mad)

    # 4. Compute expected anomalies for thresholds 1 to 5
    expected_anomalies = {}
    for t in range(1, 6):
        anomalies = sum(1 for v in imputed_values if abs(v - rounded_mean) > t * rounded_mad)
        expected_anomalies[t] = anomalies

    thresholds_found = set()
    for item in data:
        assert "threshold" in item, "Missing 'threshold' key in JSON object."
        assert "anomalies" in item, "Missing 'anomalies' key in JSON object."
        assert "time_ms" in item, "Missing 'time_ms' key in JSON object."

        t = item["threshold"]
        thresholds_found.add(t)

        expected_count = expected_anomalies.get(t, None)
        assert expected_count is not None, f"Unexpected threshold {t} found in JSON."
        assert item["anomalies"] == expected_count, (
            f"Incorrect anomalies count for threshold {t}. "
            f"Expected {expected_count}, got {item['anomalies']}."
        )

        assert isinstance(item["time_ms"], int), f"time_ms should be an integer for threshold {t}."
        assert item["time_ms"] >= 0, f"time_ms should be non-negative for threshold {t}."

    assert thresholds_found == {1, 2, 3, 4, 5}, "JSON must contain exactly results for thresholds 1, 2, 3, 4, and 5."