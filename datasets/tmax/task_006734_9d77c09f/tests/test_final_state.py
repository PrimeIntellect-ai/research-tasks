# test_final_state.py
import os
import csv
import pytest

def test_cpp_file_exists():
    cpp_file = "/home/user/etl_pipeline.cpp"
    assert os.path.isfile(cpp_file), f"C++ source file {cpp_file} is missing."

def test_output_file_exists():
    output_file = "/home/user/output/aligned_5min.csv"
    assert os.path.isfile(output_file), f"Output file {output_file} is missing. Did the program run and generate it?"

def test_output_content():
    output_file = "/home/user/output/aligned_5min.csv"
    assert os.path.isfile(output_file), "Output file missing."

    with open(output_file, 'r', newline='') as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            pytest.fail("Output file is empty.")

        assert header == ["bucket", "temp_avg", "humidity_avg"], f"Header is incorrect. Got: {header}"

        rows = list(reader)

    # We expect exactly 2 rows
    assert len(rows) == 2, f"Expected exactly 2 data rows, but got {len(rows)}."

    # Convert to a dictionary for order-independent checking
    data_dict = {row[0]: (row[1], row[2]) for row in rows}

    expected_data = {
        "2023-10-01T10:00:00Z": ("21.00", "55.00"),
        "2023-10-01T10:05:00Z": ("20.00", "60.00")
    }

    for bucket, expected_vals in expected_data.items():
        assert bucket in data_dict, f"Missing bucket {bucket} in the output."
        actual_vals = data_dict[bucket]
        assert actual_vals[0] == expected_vals[0], f"Incorrect temp_avg for bucket {bucket}. Expected {expected_vals[0]}, got {actual_vals[0]}."
        assert actual_vals[1] == expected_vals[1], f"Incorrect humidity_avg for bucket {bucket}. Expected {expected_vals[1]}, got {actual_vals[1]}."

    # Ensure no extra buckets were included
    for bucket in data_dict:
        assert bucket in expected_data, f"Unexpected bucket {bucket} found in the output."