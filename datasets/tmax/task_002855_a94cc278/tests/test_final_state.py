# test_final_state.py

import os
import subprocess
import pytest

def test_solution_txt_content():
    solution_path = "/home/user/solution.txt"
    assert os.path.isfile(solution_path), f"Solution file {solution_path} is missing."

    with open(solution_path, "r") as f:
        lines = [line.strip() for line in f.read().strip().splitlines()]

    assert len(lines) >= 2, "solution.txt must contain at least two lines."
    assert lines[0] == "app_03.log", f"Line 1 of solution.txt is incorrect. Expected 'app_03.log', got '{lines[0]}'."
    assert lines[1] == "63", f"Line 2 of solution.txt is incorrect. Expected '63', got '{lines[1]}'."

def test_log_ingestor_c_contains_assert():
    c_file_path = "/home/user/log_ingestor.c"
    assert os.path.isfile(c_file_path), f"Source file {c_file_path} is missing."

    with open(c_file_path, "r") as f:
        content = f.read()

    assert "assert(" in content, "log_ingestor.c must contain an assert() statement."

def test_log_ingestor_compiles_and_runs():
    binary_path = "/home/user/log_ingestor"
    assert os.path.isfile(binary_path), f"Compiled binary {binary_path} is missing. Did you recompile?"
    assert os.access(binary_path, os.X_OK), f"Binary {binary_path} is not executable."

    log_file = "/home/user/logs/app_03.log"
    assert os.path.isfile(log_file), f"Log file {log_file} is missing."

    # Run the binary against the previously crashing log file
    try:
        result = subprocess.run([binary_path, log_file], capture_output=True, text=True, timeout=5)
        assert result.returncode == 0, f"log_ingestor crashed or returned non-zero exit code {result.returncode} when processing {log_file}."
    except subprocess.TimeoutExpired:
        pytest.fail("log_ingestor timed out when processing the log file.")