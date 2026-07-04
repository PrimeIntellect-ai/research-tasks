# test_final_state.py

import os
import stat
import pytest

def test_process_c_exists():
    assert os.path.isfile("/home/user/process.c"), "/home/user/process.c does not exist."

def test_run_sh_exists_and_executable():
    file_path = "/home/user/run.sh"
    assert os.path.isfile(file_path), f"{file_path} does not exist."

    # Check if executable
    st = os.stat(file_path)
    assert bool(st.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)), f"{file_path} is not executable."

def test_run_sh_contents():
    with open("/home/user/run.sh", "r") as f:
        content = f.read()

    assert "gcc" in content, "run.sh does not contain 'gcc'"
    assert "/usr/bin/time" in content, "run.sh does not contain '/usr/bin/time'"
    assert "join" in content, "run.sh does not contain 'join'"

def test_bench_txt_exists():
    assert os.path.isfile("/home/user/bench.txt"), "/home/user/bench.txt does not exist."
    assert os.path.getsize("/home/user/bench.txt") > 0, "/home/user/bench.txt is empty."

def test_final_csv_content():
    file_path = "/home/user/final.csv"
    assert os.path.isfile(file_path), f"{file_path} does not exist."

    with open(file_path, "r") as f:
        content = f.read().strip()

    expected_lines = [
        "1,12,100",
        "3,22,200",
        "4,24,300"
    ]

    actual_lines = [line.strip() for line in content.splitlines() if line.strip()]

    # Sometimes join outputs with spaces if -t, is missed, but the prompt says:
    # "The format should be id,xor_hash,legacy_hash."
    # We will strictly check for commas.
    assert actual_lines == expected_lines, f"Content of {file_path} does not match the expected joined output."