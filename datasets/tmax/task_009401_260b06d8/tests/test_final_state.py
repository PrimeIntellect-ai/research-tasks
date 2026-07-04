# test_final_state.py
import os
import json
import subprocess
import pytest

REPORT_PATH = "/home/user/investigation_report.json"
EXPECTED_REPORT_PATH = "/tmp/expected_report.json"
REPO_PATH = "/home/user/data_service"

def test_report_exists():
    assert os.path.isfile(REPORT_PATH), f"Report file {REPORT_PATH} was not created."

def test_report_content():
    assert os.path.isfile(EXPECTED_REPORT_PATH), f"Expected report file {EXPECTED_REPORT_PATH} is missing."

    with open(EXPECTED_REPORT_PATH, 'r') as f:
        expected_data = json.load(f)

    with open(REPORT_PATH, 'r') as f:
        try:
            student_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {REPORT_PATH} is not valid JSON.")

    assert "bad_commit" in student_data, "Missing 'bad_commit' in report."
    assert student_data["bad_commit"] == expected_data["bad_commit"], f"Incorrect bad_commit. Expected {expected_data['bad_commit']}, got {student_data['bad_commit']}"

    assert "leaking_c_function" in student_data, "Missing 'leaking_c_function' in report."
    assert student_data["leaking_c_function"] == expected_data["leaking_c_function"], f"Incorrect leaking_c_function. Expected {expected_data['leaking_c_function']}, got {student_data['leaking_c_function']}"

    assert "system_call_leaking" in student_data, "Missing 'system_call_leaking' in report."
    assert student_data["system_call_leaking"].strip().lower() == expected_data["system_call_leaking"], f"Incorrect system_call_leaking. Expected {expected_data['system_call_leaking']}, got {student_data['system_call_leaking']}"

def test_git_checked_out_to_main():
    result = subprocess.run(
        ["git", "-C", REPO_PATH, "branch", "--show-current"], 
        capture_output=True, 
        text=True
    )
    assert result.returncode == 0, "Failed to run git branch in repository."
    current_branch = result.stdout.strip()

    # Check if we are on a branch (not detached HEAD)
    assert current_branch != "", "Repository is in detached HEAD state. It should be checked out to the main/master branch."
    assert current_branch in ["main", "master"], f"Repository is checked out to '{current_branch}', expected 'main' or 'master'."