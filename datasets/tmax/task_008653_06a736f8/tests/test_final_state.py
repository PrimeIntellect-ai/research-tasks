# test_final_state.py

import os
import stat
import pytest

def test_run_app_sh_executable():
    path = "/home/user/run_app.sh"
    assert os.path.isfile(path), f"Script {path} does not exist. Did you create it?"
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {path} is not executable."

def test_migrate_sh_executable():
    path = "/home/user/migrate.sh"
    assert os.path.isfile(path), f"Script {path} does not exist. Did you create it?"
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {path} is not executable."

def test_symlink_correct():
    symlink_path = "/home/user/clibs/libmatrix.so"
    assert os.path.islink(symlink_path), f"{symlink_path} is not a symlink."

    target = os.readlink(symlink_path)
    expected_targets = ["libmatrix.so.1.8.5", "/home/user/clibs/libmatrix.so.1.8.5"]
    assert target in expected_targets, f"Symlink points to incorrect version: {target}. Expected libmatrix.so.1.8.5"

def test_output_log_exists():
    log_path = "/home/user/output_v1.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist. Did math_runner execute successfully?"

def test_final_csv_correct():
    csv_path = "/home/user/final_v2.csv"
    assert os.path.isfile(csv_path), f"CSV file {csv_path} does not exist. Did migrate.sh run successfully?"

    with open(csv_path, "r") as f:
        content = f.read().strip().splitlines()

    assert len(content) == 6, f"Expected 6 lines in {csv_path} (1 header + 5 data rows), but found {len(content)}."

    assert content[0] == "MatrixID,Determinant,WorkerID", f"Incorrect header in {csv_path}. Found: {content[0]}"

    expected_data = [
        "1003,105.7,3",
        "1002,42.00,2",
        "1004,14.22,4",
        "1005,8.11,4",
        "1001,-99.50,1"
    ]

    for i, expected_line in enumerate(expected_data):
        assert content[i+1] == expected_line, f"Line {i+2} in {csv_path} is incorrect. Expected '{expected_line}', found '{content[i+1]}'."