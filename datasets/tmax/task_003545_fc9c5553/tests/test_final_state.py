# test_final_state.py

import os
import stat
import subprocess
import pytest

def test_minimal_txt_content():
    path = "/home/user/minimal.txt"
    assert os.path.isfile(path), f"File {path} is missing. You must save the minimal set of commands here."

    with open(path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = ["ALLOC", "FREE", "PROCESS"]
    assert lines == expected_lines, f"The contents of {path} are incorrect. Expected exactly the minimal commands to trigger the crash."

def test_crash_func_txt_content():
    path = "/home/user/crash_func.txt"
    assert os.path.isfile(path), f"File {path} is missing. You must write the crashing function name here."

    with open(path, "r") as f:
        content = f.read().strip()

    assert content == "cmd_process", f"The function name in {path} is incorrect. Did you identify the correct function where the segfault occurs?"

def test_poc_py_exists_and_executable():
    path = "/home/user/poc.py"
    assert os.path.isfile(path), f"File {path} is missing. You must create your regression test script here."

    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR) or bool(st.st_mode & stat.S_IXGRP) or bool(st.st_mode & stat.S_IXOTH), \
        f"File {path} is not executable. Please run chmod +x on it."

def test_poc_py_execution():
    path = "/home/user/poc.py"
    assert os.path.isfile(path), f"File {path} is missing."

    try:
        result = subprocess.run([path], capture_output=True, timeout=10)
    except subprocess.TimeoutExpired:
        pytest.fail(f"Execution of {path} timed out. It should run and exit quickly.")
    except Exception as e:
        pytest.fail(f"Failed to execute {path}: {e}")

    assert result.returncode == 0, \
        f"Running {path} did not yield exit code 0 (got {result.returncode}). It must exit with 0 if the vulnerability is successfully triggered."