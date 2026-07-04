# test_final_state.py

import os
import pytest

def test_model_fit_c_exists():
    file_path = "/home/user/model_fit.c"
    assert os.path.isfile(file_path), f"File {file_path} is missing."

def test_pipeline_sh_exists_and_executable():
    file_path = "/home/user/pipeline.sh"
    assert os.path.isfile(file_path), f"File {file_path} is missing."
    assert os.access(file_path, os.X_OK), f"File {file_path} is not executable."

def test_refined_cells_txt_exists():
    file_path = "/home/user/refined_cells.txt"
    assert os.path.isfile(file_path), f"File {file_path} is missing. Did you run pipeline.sh?"

def test_refined_cells_txt_content():
    file_path = "/home/user/refined_cells.txt"
    assert os.path.isfile(file_path), f"File {file_path} is missing."

    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "LEVEL1,0.000,0.500,0.000,0.500,2.222",
        "LEVEL2,0.000,0.250,0.000,0.250,4.000"
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in {file_path}, but found {len(lines)}."

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Line {i+1} mismatch. Expected '{expected}', got '{actual}'."