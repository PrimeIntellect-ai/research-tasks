# test_final_state.py

import os
import subprocess
import pytest

REPO_DIR = "/home/user/uptime_monitor"
REPORT_FILE = "/home/user/debugging_report.txt"
COMMITS_FILE = "/tmp/commits.txt"

def get_bad_commit_hash():
    assert os.path.isfile(COMMITS_FILE), "Setup error: /tmp/commits.txt is missing."
    with open(COMMITS_FILE, "r") as f:
        for line in f:
            if line.startswith("Bad commit:"):
                return line.split(":")[1].strip()
    pytest.fail("Setup error: Bad commit hash not found in /tmp/commits.txt")

def test_debugging_report_exists_and_format():
    assert os.path.isfile(REPORT_FILE), f"Report file {REPORT_FILE} does not exist."
    with open(REPORT_FILE, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) >= 3, f"Report file should have exactly 3 lines, found {len(lines)}."

def test_debugging_report_content():
    assert os.path.isfile(REPORT_FILE), f"Report file {REPORT_FILE} does not exist."
    with open(REPORT_FILE, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) >= 3, "Report file does not have enough lines."

    expected_hash = get_bad_commit_hash()
    actual_hash = lines[0]
    assert actual_hash == expected_hash, f"Line 1: Expected commit hash {expected_hash}, got {actual_hash}."

    actual_function = lines[1]
    assert actual_function == "calculate_weighted_average", f"Line 2: Expected 'calculate_weighted_average', got '{actual_function}'."

    actual_output = lines[2]
    assert actual_output == "Success", f"Line 3: Expected 'Success', got '{actual_output}'."

def test_fix_is_applied_and_tests_pass():
    # Verify the test input still contains a 0 weight (so the bug wasn't bypassed by changing the test)
    test_input_path = os.path.join(REPO_DIR, "test_input.txt")
    assert os.path.isfile(test_input_path), f"{test_input_path} is missing."

    with open(test_input_path, "r") as f:
        content = f.read()

    has_zero_weight = False
    for line in content.strip().split("\n"):
        parts = line.split()
        if len(parts) >= 2 and parts[1] == "0":
            has_zero_weight = True
            break

    assert has_zero_weight, "The test_input.txt file was modified to remove the 0 weight. You must fix the code, not the test input."

    # Run the test script
    run_script = os.path.join(REPO_DIR, "run_test.sh")
    assert os.access(run_script, os.X_OK), f"{run_script} is not executable."

    result = subprocess.run(
        ["./run_test.sh"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"./run_test.sh failed with return code {result.returncode}.\nStdout: {result.stdout}\nStderr: {result.stderr}"
    assert "Success" in result.stdout, f"Expected 'Success' in output, but got:\n{result.stdout}"