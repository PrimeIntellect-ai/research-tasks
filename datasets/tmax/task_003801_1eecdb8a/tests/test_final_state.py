# test_final_state.py
import os
import csv
import math

def test_script_exists_and_executable():
    path = "/home/user/profile_pipeline.sh"
    assert os.path.isfile(path), f"Script {path} is missing."
    assert os.access(path, os.X_OK), f"Script {path} is not executable."

    with open(path, "r") as f:
        content = f.read()
    assert "h5dump" in content, "Script does not use 'h5dump' as required."

def test_csv_results():
    csv_path = "/home/user/profiling_results.csv"
    assert os.path.isfile(csv_path), f"CSV file {csv_path} is missing."

    with open(csv_path, "r") as f:
        reader = list(csv.reader(f))

    assert len(reader) == 5, f"Expected exactly 5 lines in the CSV, found {len(reader)}."

    header = reader[0]
    expected_header = ["Level", "Length", "DensityPeak", "Time", "Rate"]
    assert header == expected_header, f"Expected header {expected_header}, got {header}."

    expected_levels = [2, 4, 8, 16]

    for i, row in enumerate(reader[1:]):
        assert len(row) == 5, f"Row {i+1} does not have exactly 5 columns."
        level = int(row[0])
        length = int(row[1])
        density_peak = float(row[2])
        time_val = float(row[3])
        rate = float(row[4])

        assert level == expected_levels[i], f"Row {i+1} expected level {expected_levels[i]}, got {level}."
        assert length == 5000, f"Row {i+1} expected length 5000, got {length}."

        expected_peak = 999.9 / level
        assert math.isclose(density_peak, expected_peak, rel_tol=1e-3), f"Row {i+1} expected DensityPeak ~{expected_peak}, got {density_peak}."

        assert time_val > 0, f"Row {i+1} time should be greater than 0."

        expected_rate = length / time_val
        assert math.isclose(rate, expected_rate, rel_tol=0.05), f"Row {i+1} expected Rate ~{expected_rate}, got {rate}."