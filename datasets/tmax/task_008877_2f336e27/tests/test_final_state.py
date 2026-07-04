# test_final_state.py

import os
import stat
import pytest

def test_pipeline_sh_exists_and_executable():
    file_path = "/home/user/pipeline.sh"
    assert os.path.isfile(file_path), f"File {file_path} is missing."
    st = os.stat(file_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"File {file_path} is not executable."

def test_venv_exists():
    venv_path = "/home/user/venv"
    assert os.path.isdir(venv_path), f"Virtual environment directory {venv_path} is missing."
    python_bin = os.path.join(venv_path, "bin", "python")
    assert os.path.isfile(python_bin), f"Python executable in venv is missing at {python_bin}."

def test_processed_dir_exists():
    processed_dir = "/home/user/processed"
    assert os.path.isdir(processed_dir), f"Directory {processed_dir} is missing."

def test_final_features_csv():
    file_path = "/home/user/final_features.csv"
    assert os.path.isfile(file_path), f"File {file_path} is missing."

    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "id,feature_alpha,feature_beta,target",
        "1,1.0,1.2,0",
        "2,0.2,0.8,1",
        "3,1.8,1.1,1",
        "4,0.8,0.5,0"
    ]

    assert len(lines) == 5, f"Expected 5 lines in {file_path}, but got {len(lines)}."

    # Check header
    assert lines[0] == expected_lines[0], f"Header mismatch in {file_path}. Expected {expected_lines[0]} but got {lines[0]}."

    # Check data (order might vary depending on how they merged, but usually sequential)
    data_lines = sorted(lines[1:])
    expected_data = sorted(expected_lines[1:])
    assert data_lines == expected_data, f"Data mismatch in {file_path}. Expected {expected_data} but got {data_lines}."

def test_row_count_txt():
    file_path = "/home/user/row_count.txt"
    assert os.path.isfile(file_path), f"File {file_path} is missing."

    with open(file_path, "r") as f:
        content = f.read().strip()

    assert content == "4", f"Expected row count to be '4', but got '{content}'."