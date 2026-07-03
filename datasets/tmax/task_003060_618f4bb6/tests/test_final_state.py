# test_final_state.py

import os
import stat

def test_cleaned_data_correctness():
    cleaned_data_path = "/home/user/cleaned_data.csv"
    assert os.path.isfile(cleaned_data_path), f"File not found: {cleaned_data_path}"

    with open(cleaned_data_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "1.0,2.1",
        "2.0,4.0",
        "3.0,6.1",
        "4.0,8.0"
    ]

    assert len(lines) == 4, f"Expected 4 lines in cleaned_data.csv, found {len(lines)}"
    for expected in expected_lines:
        assert expected in lines, f"Expected line '{expected}' not found in cleaned_data.csv"

    # Also check that filtered out lines are not present
    content = "\n".join(lines)
    assert "X,Y" not in content, "Header was not removed from cleaned_data.csv"
    assert "NaN" not in content, "'NaN' rows were not removed from cleaned_data.csv"
    assert "-1.5" not in content, "Negative X values were not removed from cleaned_data.csv"
    assert "-0.5" not in content, "Negative X values were not removed from cleaned_data.csv"

def test_compiled_executable_exists():
    executable_path = "/home/user/train_model"
    assert os.path.isfile(executable_path), f"Executable not found: {executable_path}"

    # Check if it's executable
    st = os.stat(executable_path)
    assert bool(st.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)), f"File is not executable: {executable_path}"

def test_model_output_correctness():
    output_path = "/home/user/model_output.txt"
    assert os.path.isfile(output_path), f"File not found: {output_path}"

    with open(output_path, 'r') as f:
        content = f.read()

    assert "Slope: 1.98" in content, "Slope value is incorrect or missing in model_output.txt"
    assert "Intercept: 0.1" in content, "Intercept value is incorrect or missing in model_output.txt"