# test_final_state.py

import os
import subprocess
import pytest

def test_incident_report():
    report_path = "/home/user/incident_report.txt"
    assert os.path.exists(report_path), "Incident report /home/user/incident_report.txt is missing."

    with open(report_path, "r") as f:
        lines = [line.strip() for line in f.read().strip().split('\n') if line.strip()]

    assert len(lines) == 3, f"Incident report must have exactly 3 lines, found {len(lines)}."

    with open("/home/user/.expected_secret", "r") as f:
        expected_secret = f.read().strip()
    with open("/home/user/.expected_commit", "r") as f:
        expected_commit = f.read().strip()
    with open("/home/user/.expected_record", "r") as f:
        expected_record = f.read().strip()

    assert lines[0] == expected_secret, f"Line 1 (Secret API key) is incorrect. Expected {expected_secret}, got {lines[0]}."
    assert lines[1] == expected_commit, f"Line 2 (Commit hash) is incorrect. Expected {expected_commit}, got {lines[1]}."
    assert lines[2] == expected_record, f"Line 3 (Dropped record ID) is incorrect. Expected {expected_record}, got {lines[2]}."

def test_regression_test_and_fix():
    repo_dir = "/home/user/pipeline_repo"
    test_file = os.path.join(repo_dir, "test_processor.cpp")
    processor_file = os.path.join(repo_dir, "processor.cpp")

    assert os.path.exists(test_file), "/home/user/pipeline_repo/test_processor.cpp is missing."
    assert os.path.exists(processor_file), "/home/user/pipeline_repo/processor.cpp is missing."

    # 1. Compile and run with user's processor.cpp (should be fixed)
    compile_cmd = ["g++", "-std=c++17", "test_processor.cpp", "processor.cpp", "-o", "test_runner"]
    res = subprocess.run(compile_cmd, cwd=repo_dir, capture_output=True)
    assert res.returncode == 0, f"Compilation failed for the fixed pipeline: {res.stderr.decode()}"

    run_res = subprocess.run(["./test_runner"], cwd=repo_dir)
    assert run_res.returncode == 0, "Test runner failed (returned non-zero) on the fixed processor.cpp. The bug might not be fixed or the test is incorrect."

    # 2. Compile and run with buggy processor.cpp to verify test validity
    buggy_cpp = """#include "processor.h"

bool isValidRecord(const Record& r, long window_start, long window_end) {
    return r.timestamp > window_start && r.timestamp < window_end;
}
"""

    # Backup user's processor.cpp
    with open(processor_file, "r") as f:
        user_cpp = f.read()

    try:
        with open(processor_file, "w") as f:
            f.write(buggy_cpp)

        res = subprocess.run(compile_cmd, cwd=repo_dir, capture_output=True)
        assert res.returncode == 0, f"Compilation of buggy version failed: {res.stderr.decode()}"

        run_res = subprocess.run(["./test_runner"], cwd=repo_dir)
        assert run_res.returncode != 0, "Regression test passed (returned 0) on the buggy processor.cpp. The test does not properly catch the boundary condition bug."
    finally:
        # Restore user's processor.cpp
        with open(processor_file, "w") as f:
            f.write(user_cpp)