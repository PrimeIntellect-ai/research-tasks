# test_final_state.py

import os
import pytest

def test_renamed_files_exist():
    """Test that the files have been extracted and renamed properly."""
    renamed_dir = "/home/user/renamed"
    assert os.path.isdir(renamed_dir), f"Directory {renamed_dir} does not exist."

    expected_files = []
    id_counter = 100
    for b in range(1, 3):
        for z in range(1, 3):
            for f in range(1, 4):
                id_counter += 1
                date_str = f"2023-01-{f:02d}"
                filename = f"data_{date_str}_{id_counter}.txt"
                expected_files.append(filename)

    actual_files = set(os.listdir(renamed_dir))
    for expected_file in expected_files:
        assert expected_file in actual_files, f"Expected renamed file {expected_file} is missing in {renamed_dir}"

def test_master_csv_contents():
    """Test that the master.csv contains the correct processed data lines."""
    master_csv_path = "/home/user/final/master.csv"
    assert os.path.isfile(master_csv_path), f"Final output file {master_csv_path} does not exist."

    expected_lines = []
    id_counter = 100
    for b in range(1, 3):
        for z in range(1, 3):
            for f in range(1, 4):
                id_counter += 1
                expected_lines.append(f"{id_counter},val{id_counter}A,val{id_counter}B,val{id_counter}C")
                expected_lines.append(f"{id_counter},val{id_counter}X,val{id_counter}Y,val{id_counter}Z")

    with open(master_csv_path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert len(actual_lines) == 24, f"Expected 24 lines in master.csv, but found {len(actual_lines)}."

    expected_set = set(expected_lines)
    actual_set = set(actual_lines)

    missing_lines = expected_set - actual_set
    extra_lines = actual_set - expected_set

    assert not missing_lines, f"Missing expected lines in master.csv: {missing_lines}"
    assert not extra_lines, f"Found unexpected lines in master.csv: {extra_lines}"