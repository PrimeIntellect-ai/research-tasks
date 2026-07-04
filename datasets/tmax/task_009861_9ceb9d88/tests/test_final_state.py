# test_final_state.py

import os
import stat
import pytest

def test_compute_negatives_c_exists():
    file_path = "/home/user/compute_negatives.c"
    assert os.path.exists(file_path), f"The file {file_path} is missing."
    assert os.path.isfile(file_path), f"The path {file_path} is not a file."

def test_track_experiment_sh_executable():
    file_path = "/home/user/track_experiment.sh"
    assert os.path.exists(file_path), f"The file {file_path} is missing."
    assert os.path.isfile(file_path), f"The path {file_path} is not a file."

    st = os.stat(file_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"The file {file_path} is not executable."

def test_hard_negatives_csv_content():
    file_path = "/home/user/data/hard_negatives.csv"
    assert os.path.exists(file_path), f"The file {file_path} is missing."

    expected_content = (
        "id,hard_negative_id,score\n"
        "1,2,0.9000\n"
        "2,1,0.9000\n"
        "3,4,0.9000\n"
        "4,3,0.9000"
    )

    with open(file_path, "r") as f:
        content = f.read().strip()

    assert content == expected_content, f"The content of {file_path} is incorrect. Expected:\n{expected_content}\nGot:\n{content}"

def test_experiment_log_content():
    file_path = "/home/user/experiment.log"
    assert os.path.exists(file_path), f"The file {file_path} is missing."

    expected_line = "[Experiment CL-01] AvgScore=0.9000"

    with open(file_path, "r") as f:
        lines = f.readlines()

    found = any(expected_line in line for line in lines)
    assert found, f"The file {file_path} does not contain the expected line: '{expected_line}'"