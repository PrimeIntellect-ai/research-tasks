# test_final_state.py

import os
import re
import pytest

def test_analyze_script_exists_and_executable():
    script_path = "/home/user/analyze.sh"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"The script {script_path} is not executable."

def test_joined_csv():
    file_path = "/home/user/joined.csv"
    assert os.path.isfile(file_path), f"The file {file_path} does not exist."

    with open(file_path, "r") as f:
        lines = f.read().strip().split("\n")

    assert len(lines) == 16, f"Expected 16 lines in {file_path} (1 header + 15 data rows), found {len(lines)}."
    assert lines[0] == "user_id,age,income,spend", f"Incorrect header in {file_path}."

    # Check if a random row is joined correctly
    # e.g., 1,25,50000,1000
    has_row_1 = any(line == "1,25,50000,1000" for line in lines)
    assert has_row_1, f"Expected joined data '1,25,50000,1000' not found in {file_path}."

@pytest.mark.parametrize("sample_num", [1, 2, 3])
def test_sample_csvs(sample_num):
    file_path = f"/home/user/sample_{sample_num}.csv"
    assert os.path.isfile(file_path), f"The file {file_path} does not exist."

    with open(file_path, "r") as f:
        lines = f.read().strip().split("\n")

    assert len(lines) == 16, f"Expected 16 lines in {file_path} (1 header + 15 data rows), found {len(lines)}."
    assert lines[0] == "user_id,age,income,spend", f"Incorrect header in {file_path}."

    # Check that all data rows have 4 columns
    for i, line in enumerate(lines[1:], start=2):
        cols = line.split(",")
        assert len(cols) == 4, f"Row {i} in {file_path} does not have exactly 4 columns."

def test_best_alphas_txt():
    file_path = "/home/user/best_alphas.txt"
    assert os.path.isfile(file_path), f"The file {file_path} does not exist."

    with open(file_path, "r") as f:
        lines = f.read().strip().split("\n")

    assert len(lines) == 3, f"Expected exactly 3 lines in {file_path}, found {len(lines)}."

    expected_pattern = r"^Sample [1-3]: (0\.1|1\.0|10\.0)$"
    samples_found = set()

    for i, line in enumerate(lines):
        match = re.match(expected_pattern, line)
        assert match, f"Line {i+1} in {file_path} does not match expected format: '{line}'"
        samples_found.add(line.split(":")[0])

    assert samples_found == {"Sample 1", "Sample 2", "Sample 3"}, f"Missing or duplicate samples in {file_path}."