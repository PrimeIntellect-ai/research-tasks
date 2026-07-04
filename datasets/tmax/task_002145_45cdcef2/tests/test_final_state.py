# test_final_state.py
import os
import json
import csv
import math

def test_experiment_log_and_parquet_exist():
    parquet_path = "/home/user/processed_data.parquet"
    json_path = "/home/user/experiment_log.json"

    assert os.path.isfile(parquet_path), f"Parquet file {parquet_path} was not created."
    assert os.path.getsize(parquet_path) > 0, f"Parquet file {parquet_path} is empty."

    assert os.path.isfile(json_path), f"JSON log file {json_path} was not created."
    assert os.path.getsize(json_path) > 0, f"JSON log file {json_path} is empty."

def test_experiment_log_contents():
    csv_path = "/home/user/raw_dataset.csv"
    json_path = "/home/user/experiment_log.json"

    # Recompute expected values from the raw CSV
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    initial_rows = len(rows)
    valid_ages = []
    cleaned_rows = 0

    for row in rows:
        text = row.get("text", "")
        # Drop if missing or empty string
        if text is None or text == "":
            continue
        cleaned_rows += 1

        age_str = row.get("author_age", "")
        try:
            age = float(age_str)
            if 15 <= age <= 100:
                valid_ages.append(age)
        except ValueError:
            pass

    valid_ages.sort()
    n = len(valid_ages)
    assert n > 0, "No valid ages found to compute median."

    if n % 2 == 1:
        expected_median = float(valid_ages[n // 2])
    else:
        expected_median = (valid_ages[n // 2 - 1] + valid_ages[n // 2]) / 2.0

    # Read the JSON log
    with open(json_path, "r", encoding="utf-8") as f:
        try:
            log = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {json_path} is not valid JSON."

    # Assert keys exist
    expected_keys = {"initial_rows", "cleaned_rows", "median_age_used", "explained_variance_ratio_sum"}
    actual_keys = set(log.keys())
    assert actual_keys == expected_keys, f"JSON keys mismatch. Expected {expected_keys}, got {actual_keys}"

    # Assert computed values
    assert log["initial_rows"] == initial_rows, f"Expected initial_rows={initial_rows}, got {log['initial_rows']}"
    assert log["cleaned_rows"] == cleaned_rows, f"Expected cleaned_rows={cleaned_rows}, got {log['cleaned_rows']}"
    assert math.isclose(float(log["median_age_used"]), expected_median, abs_tol=1e-5), \
        f"Expected median_age_used={expected_median}, got {log['median_age_used']}"

    # Assert PCA explained variance ratio sum is a reasonable float (around 0.08)
    evr_sum = log["explained_variance_ratio_sum"]
    assert isinstance(evr_sum, float), f"explained_variance_ratio_sum must be a float, got {type(evr_sum)}"
    assert 0.05 < evr_sum < 0.15, f"explained_variance_ratio_sum {evr_sum} is outside the expected plausible range (0.05 - 0.15)."