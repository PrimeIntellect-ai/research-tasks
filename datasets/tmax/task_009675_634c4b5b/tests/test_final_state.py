# test_final_state.py

import os
import subprocess
import time
import re

def test_regression_report():
    report_path = "/home/user/regression_report.txt"
    hash_file = "/tmp/.bad_commit_hash"

    assert os.path.exists(report_path), f"Report file {report_path} is missing."
    assert os.path.exists(hash_file), f"Truth file {hash_file} is missing."

    with open(hash_file, "r") as f:
        bad_commit = f.read().strip()

    with open(report_path, "r") as f:
        report_content = f.read()

    assert f"Bad Commit: {bad_commit}" in report_content, "The regression report does not contain the correct bad commit hash."
    assert "Status: fixed" in report_content, "The regression report does not contain 'Status: fixed'."

def test_process_logs_performance_and_output():
    script_path = "/home/user/log_processor/process_logs.sh"
    log_file = "/home/user/large_logs.txt"

    assert os.path.exists(script_path), f"Script {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    # Generate expected output
    with open(log_file, "r") as f:
        log_lines = f.readlines()

    expected_lines = [line for line in log_lines if "ERROR" in line or "WARNING" in line]
    expected_output = "".join(expected_lines) + "\n"

    start_time = time.time()
    result = subprocess.run(
        ["bash", script_path, log_file],
        capture_output=True,
        text=True
    )
    end_time = time.time()
    duration = end_time - start_time

    assert result.returncode == 0, f"Script failed with return code {result.returncode}."
    assert duration < 1.5, f"Script execution took {duration:.2f} seconds, which is strictly >= 1.5 seconds."
    assert result.stdout == expected_output, "Script output does not match the expected output (make sure to include the trailing newline from commit 4)."

def test_git_state():
    repo_dir = "/home/user/log_processor"

    # Check if we are on main branch
    result = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        cwd=repo_dir,
        capture_output=True,
        text=True,
        check=True
    )
    branch = result.stdout.strip()
    assert branch == "main", f"Expected to be on 'main' branch, but currently on '{branch}'."

    # Check if working tree is clean (changes committed)
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=repo_dir,
        capture_output=True,
        text=True,
        check=True
    )
    assert not result.stdout.strip(), "There are uncommitted changes in the repository. Please commit your fix."