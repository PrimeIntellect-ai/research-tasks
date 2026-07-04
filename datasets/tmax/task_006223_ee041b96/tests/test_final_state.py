# test_final_state.py
import os
import json
import subprocess
import pytest

def test_debugging_report():
    report_path = "/home/user/debugging_report.json"
    assert os.path.exists(report_path), f"Report file {report_path} does not exist."

    with open(report_path, "r") as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {report_path} is not valid JSON.")

    assert "bad_commit" in report, "Key 'bad_commit' missing from report."
    assert "missing_file" in report, "Key 'missing_file' missing from report."

    # Get the expected bad commit from git history
    repo_path = "/home/user/log_processor"
    result = subprocess.run(
        ["git", "log", "--grep=Feature: Add override config support for critical logs", "--format=%H"],
        cwd=repo_path, capture_output=True, text=True, check=True
    )
    expected_commit = result.stdout.strip()
    assert expected_commit, "Could not find the expected commit in git history."

    assert report["bad_commit"] == expected_commit, f"Incorrect bad_commit. Expected {expected_commit}, got {report['bad_commit']}."

    expected_file = "/etc/log_processor/features.conf"
    assert report["missing_file"] == expected_file, f"Incorrect missing_file. Expected {expected_file}, got {report['missing_file']}."

def test_bisect_script():
    script_path = "/home/user/bisect_test.sh"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."