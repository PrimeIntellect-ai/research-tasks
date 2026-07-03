# test_final_state.py

import os
import json
import math

def test_pipeline_script_exists_and_executable():
    """Verify the pipeline script exists and is executable."""
    script_path = "/home/user/pipeline.sh"
    assert os.path.exists(script_path), f"Pipeline script {script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a file."
    assert os.access(script_path, os.X_OK), f"Pipeline script {script_path} is not executable."

def test_cleaned_measurements_content():
    """Verify the cleaned_measurements.csv contains exactly the valid rows."""
    output_csv = "/home/user/output/cleaned_measurements.csv"
    assert os.path.exists(output_csv), f"Output file {output_csv} does not exist."

    with open(output_csv, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "id,value,category",
        "1,12.34567,A",
        "3,-9.87654,A",
        "6,45.6789,B",
        "8,0.00000,C",  # 0.0 or 0.00000 might be formatted differently, but exact match to original is safest
        "10,3.14159,C",
        "11,50.0,A"
    ]

    # We will parse the CSV to allow slight formatting differences in floats if they preserved the original string,
    # but the instructions say "maintain the original ordering for valid rows".
    # Let's check the parsed values to be robust against string formatting changes (like 0.00000 -> 0.0).
    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} rows in cleaned CSV, found {len(lines)}."
    assert lines[0] == "id,value,category", "Header of cleaned CSV is missing or incorrect."

    for i in range(1, len(expected_lines)):
        expected_parts = expected_lines[i].split(',')
        actual_parts = lines[i].split(',')

        assert len(actual_parts) == 3, f"Row {i} does not have 3 columns."
        assert actual_parts[0] == expected_parts[0], f"Row {i} ID mismatch: expected {expected_parts[0]}, got {actual_parts[0]}"
        assert actual_parts[2] == expected_parts[2], f"Row {i} category mismatch: expected {expected_parts[2]}, got {actual_parts[2]}"

        # Check float value
        expected_val = float(expected_parts[1])
        actual_val = float(actual_parts[1])
        assert math.isclose(actual_val, expected_val, rel_tol=1e-9), \
            f"Row {i} value mismatch: expected {expected_val}, got {actual_val}"

def test_stats_json_content():
    """Verify the stats.json contains the correct rounded mean and variance."""
    output_json = "/home/user/output/stats.json"
    assert os.path.exists(output_json), f"Output file {output_json} does not exist."

    with open(output_json, "r") as f:
        try:
            stats = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{output_json} is not valid JSON."

    expected_stats = {
        "A": {"mean": 17.4897, "variance": 610.7649},
        "B": {"mean": 45.6789, "variance": 0.0},
        "C": {"mean": 1.5708, "variance": 2.4674}
    }

    assert sorted(stats.keys()) == ["A", "B", "C"], "JSON keys must be exactly 'A', 'B', 'C' and alphabetically ordered."

    for cat, expected in expected_stats.items():
        assert "mean" in stats[cat], f"Missing 'mean' for category {cat}."
        assert "variance" in stats[cat], f"Missing 'variance' for category {cat}."

        actual_mean = stats[cat]["mean"]
        actual_var = stats[cat]["variance"]

        assert isinstance(actual_mean, (int, float)), f"Mean for {cat} must be a number."
        assert isinstance(actual_var, (int, float)), f"Variance for {cat} must be a number."

        assert math.isclose(actual_mean, expected["mean"], abs_tol=1e-4), \
            f"Mean for {cat} is incorrect. Expected {expected['mean']}, got {actual_mean}."

        assert math.isclose(actual_var, expected["variance"], abs_tol=1e-4), \
            f"Variance for {cat} is incorrect. Expected {expected['variance']}, got {actual_var}."