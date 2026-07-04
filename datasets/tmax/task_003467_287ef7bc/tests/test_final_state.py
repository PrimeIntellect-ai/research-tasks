# test_final_state.py

import os
import pytest
import csv

def test_run_etl_script_exists_and_executable():
    script_path = "/home/user/run_etl.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_output_csv_exists_and_correct():
    output_path = "/home/user/output/regional_load.csv"
    assert os.path.isfile(output_path), f"Output file {output_path} does not exist."

    with open(output_path, "r", newline="") as f:
        content = f.read().strip().replace("\r\n", "\n")

    expected_content = (
        "region_id,hour,sum_z_score\n"
        "Region_A,2023-10-01T10:00:00Z,-2.0000\n"
        "Region_A,2023-10-01T11:00:00Z,2.0000\n"
        "Region_B,2023-10-01T10:00:00Z,-1.0000\n"
        "Region_B,2023-10-01T11:00:00Z,1.0000"
    )

    assert content == expected_content, f"Content of {output_path} does not match the expected output. Got:\n{content}"

def test_output_csv_parsed_values():
    output_path = "/home/user/output/regional_load.csv"
    if not os.path.isfile(output_path):
        pytest.fail(f"Output file {output_path} does not exist.")

    with open(output_path, "r", newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "Output CSV is empty."
    assert rows[0] == ["region_id", "hour", "sum_z_score"], "CSV headers are incorrect."

    data_rows = rows[1:]
    assert len(data_rows) == 4, f"Expected 4 data rows, got {len(data_rows)}."

    # Check sorting
    regions = [row[0] for row in data_rows]
    hours = [row[1] for row in data_rows]

    assert regions == sorted(regions), "Rows are not sorted alphabetically by region_id."

    # Check specific values
    expected_data = [
        ["Region_A", "2023-10-01T10:00:00Z", "-2.0000"],
        ["Region_A", "2023-10-01T11:00:00Z", "2.0000"],
        ["Region_B", "2023-10-01T10:00:00Z", "-1.0000"],
        ["Region_B", "2023-10-01T11:00:00Z", "1.0000"],
    ]

    for i, (expected, actual) in enumerate(zip(expected_data, data_rows)):
        assert actual[0] == expected[0], f"Row {i+1}: Expected region {expected[0]}, got {actual[0]}"
        assert actual[1] == expected[1], f"Row {i+1}: Expected hour {expected[1]}, got {actual[1]}"

        # Check float value up to 4 decimal places
        try:
            actual_val = float(actual[2])
            expected_val = float(expected[2])
            assert abs(actual_val - expected_val) < 1e-4, f"Row {i+1}: Expected sum_z_score {expected_val}, got {actual_val}"

            # Check string formatting is exactly 4 decimal places
            decimal_part = actual[2].split('.')[-1] if '.' in actual[2] else ""
            assert len(decimal_part) == 4, f"Row {i+1}: sum_z_score must be formatted to 4 decimal places, got '{actual[2]}'"
        except ValueError:
            pytest.fail(f"Row {i+1}: sum_z_score '{actual[2]}' is not a valid float.")