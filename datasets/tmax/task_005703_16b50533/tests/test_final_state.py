# test_final_state.py

import os
import stat
import pytest

def test_dedup_c_exists():
    path = "/home/user/dedup.c"
    assert os.path.isfile(path), f"The C source file {path} does not exist."

def test_dedup_executable_exists():
    path = "/home/user/dedup"
    assert os.path.isfile(path), f"The executable {path} does not exist."
    st = os.stat(path)
    assert st.st_mode & stat.S_IXUSR, f"The file {path} is not executable."

def test_pipeline_sh_exists_and_executable():
    path = "/home/user/pipeline.sh"
    assert os.path.isfile(path), f"The bash script {path} does not exist."
    st = os.stat(path)
    assert st.st_mode & stat.S_IXUSR, f"The script {path} is not executable."

def test_sampled_csv_content():
    path = "/home/user/sampled.csv"
    assert os.path.isfile(path), f"The output file {path} does not exist."

    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "u1,admin,10",
        "u2,user,5",
        "u3,guest,2",
        "u4,user,8",
        "u5,admin,20",
        "u6,guest,1"
    ]

    # The truth script accepts either exact match or sorted match
    assert sorted(lines) == sorted(expected_lines), f"The content of {path} does not match the expected output. Got: {lines}"