# test_final_state.py

import os

def test_joined_csv_exists_and_correct():
    file_path = "/home/user/data/joined.csv"
    assert os.path.isfile(file_path), f"The file {file_path} is missing."

    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 100, f"Expected 100 lines in {file_path}, found {len(lines)}."

    # Check a few specific lines to ensure correct join
    assert lines[0] == "1,2.0,1", f"First line of joined.csv is incorrect: {lines[0]}"
    assert lines[79] == "80,160.0,0", f"80th line of joined.csv is incorrect: {lines[79]}"
    assert lines[99] == "100,200.0,0", f"Last line of joined.csv is incorrect: {lines[99]}"

def test_executable_compiled():
    exe_path = "/home/user/normalize"
    assert os.path.isfile(exe_path), f"The compiled executable {exe_path} is missing."
    assert os.access(exe_path, os.X_OK), f"The file {exe_path} is not executable."

def test_predictions_csv_correct():
    file_path = "/home/user/predictions.csv"
    assert os.path.isfile(file_path), f"The file {file_path} is missing."

    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 100, f"Expected 100 lines in {file_path}, found {len(lines)}."

    # Check the 81st row (index 80)
    # Original val1 is 162.0. Mean of first 80 is 81.0. Normalized is 81.0000. Label is 1.
    parts = lines[80].split(',')
    assert len(parts) == 3, f"81st row does not have 3 columns: {lines[80]}"
    assert parts[0] == "81", f"81st row ID is incorrect: {parts[0]}"
    assert float(parts[1]) == 81.0, f"81st row normalized value is incorrect: {parts[1]}"
    assert parts[2] == "1", f"81st row label is incorrect: {parts[2]}"

def test_mean_used_txt():
    file_path = "/home/user/mean_used.txt"
    assert os.path.isfile(file_path), f"The file {file_path} is missing."

    with open(file_path, "r") as f:
        content = f.read().strip()

    assert float(content) == 81.0, f"Expected mean used to be 81.0, found {content}."

def test_report_txt():
    file_path = "/home/user/report.txt"
    assert os.path.isfile(file_path), f"The file {file_path} is missing."

    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 lines in {file_path}, found {len(lines)}."

    assert float(lines[0]) == 81.0, f"Line 1 of report.txt (training mean) is incorrect: {lines[0]}"
    assert float(lines[1]) == 81.0, f"Line 2 of report.txt (81st row normalized value) is incorrect: {lines[1]}"