# test_final_state.py

import os
import re
import pytest

def test_pipeline_c_exists():
    file_path = "/home/user/pipeline.c"
    assert os.path.isfile(file_path), f"The file {file_path} is missing."

def test_pipeline_executable_exists():
    file_path = "/home/user/pipeline"
    assert os.path.isfile(file_path), f"The executable {file_path} is missing."
    assert os.access(file_path, os.X_OK), f"The file {file_path} is not executable."

def test_cleaned_data_csv():
    file_path = "/home/user/cleaned_data.csv"
    assert os.path.isfile(file_path), f"The file {file_path} is missing."

    expected_content = (
        "id,f1,f2,target\n"
        "1,10,20,17.50\n"
        "2,15,30,26.25\n"
        "3,20,30,27.50\n"
        "4,25,30,28.75\n"
        "5,30,40,37.50"
    )

    with open(file_path, 'r') as f:
        content = f.read().strip()

    assert content == expected_content, f"The content of {file_path} does not match the expected final state."

def test_summary_txt():
    file_path = "/home/user/summary.txt"
    assert os.path.isfile(file_path), f"The file {file_path} is missing."

    with open(file_path, 'r') as f:
        content = f.read().strip()

    lines = [line.strip() for line in content.split('\n') if line.strip()]

    assert len(lines) == 4, f"Expected 4 lines in {file_path}, but found {len(lines)}."

    assert lines[0] == "Imputed_f2_Mean: 30", f"Line 1 incorrect: {lines[0]}"
    assert lines[1] == "Target_ID_2: 26.25", f"Line 2 incorrect: {lines[1]}"
    assert lines[2] == "Target_ID_4: 28.75", f"Line 3 incorrect: {lines[2]}"

    benchmark_match = re.match(r"^Benchmark_Time_Sec: \d+\.\d{6}$", lines[3])
    assert benchmark_match, f"Line 4 does not match expected format for benchmark time: {lines[3]}"