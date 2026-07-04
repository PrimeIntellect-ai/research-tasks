# test_final_state.py

import os
import csv
import math
import pytest

def test_results_file_exists():
    """Test that the results.csv file exists in the correct location."""
    file_path = "/home/user/results.csv"
    assert os.path.isfile(file_path), f"The file {file_path} is missing. The script did not create the output file."

def test_results_file_content():
    """Test that the results.csv file contains the correct results."""
    file_path = "/home/user/results.csv"
    if not os.path.isfile(file_path):
        pytest.fail(f"The file {file_path} is missing.")

    with open(file_path, "r") as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            pytest.fail(f"The file {file_path} is empty.")

    assert header == ["sensor_id", "f", "root"], f"Incorrect header in {file_path}: {header}"

    results = {}
    with open(file_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                sid = int(row["sensor_id"])
                f_val = float(row["f"])
                root_val = float(row["root"])
                results[sid] = (f_val, root_val)
            except (ValueError, KeyError) as e:
                pytest.fail(f"Error parsing row {row}: {e}")

    assert len(results) == 4, f"Expected 4 rows of data, got {len(results)}"

    expected_values = {
        0: {"f": 3.0, "root": 0.1402},
        1: {"f": 5.0, "root": 0.0064},
        2: {"f": 7.0, "root": 0.0487},
        3: {"f": 9.0, "root": 0.0141},
    }

    for sid, expected in expected_values.items():
        assert sid in results, f"Missing results for sensor_id {sid}"
        f_val, root_val = results[sid]

        # Check frequency
        assert math.isclose(f_val, expected["f"], abs_tol=0.1), \
            f"Sensor {sid}: Expected frequency ~{expected['f']}, got {f_val}"

        # Check root
        assert math.isclose(root_val, expected["root"], abs_tol=0.01), \
            f"Sensor {sid}: Expected root ~{expected['root']}, got {root_val}"