# test_final_state.py

import os
import pytest

def test_script_exists_and_executable():
    script_path = "/home/user/organize_projects.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_extracted_projects():
    sub_001_dir = "/home/user/projects/sub_001"
    sub_005_dir = "/home/user/projects/sub_005"

    assert os.path.isdir(sub_001_dir), f"Safe project sub_001 was not extracted to {sub_001_dir}."
    assert os.path.isdir(sub_005_dir), f"Safe project sub_005 was not extracted to {sub_005_dir}."

    # Check for specific files inside to ensure extraction was successful
    # Note: extraction might include the top-level directory of the archive (e.g., proj1/main.py)
    # We'll just check if main.py is somewhere in sub_001
    sub_001_files = []
    for root, _, files in os.walk(sub_001_dir):
        sub_001_files.extend(files)
    assert "main.py" in sub_001_files, "main.py not found in extracted sub_001."

    sub_005_files = []
    for root, _, files in os.walk(sub_005_dir):
        sub_005_files.extend(files)
    assert "new.py" in sub_005_files, "new.py not found in extracted sub_005."
    assert "old.py" in sub_005_files, "old.py not found in extracted sub_005."

def test_malicious_and_rejected_not_extracted():
    not_expected_dirs = [
        "/home/user/projects/sub_002", # Rejected
        "/home/user/projects/sub_003", # Malicious
        "/home/user/projects/sub_004"  # Malicious
    ]
    for d in not_expected_dirs:
        assert not os.path.exists(d), f"Directory {d} should not exist (it was malicious or rejected)."

def test_recent_code_copied():
    recent_dir = "/home/user/recent_code"
    assert os.path.isdir(recent_dir), f"Directory {recent_dir} does not exist."

    expected_files = ["main.py", "new.py"]
    actual_files = os.listdir(recent_dir)

    for ef in expected_files:
        assert ef in actual_files, f"Recent python file {ef} was not copied to {recent_dir}."

    assert "old.py" not in actual_files, "old.py was copied, but it is older than 7 days."

def test_summary_report():
    summary_path = "/home/user/summary.txt"
    assert os.path.isfile(summary_path), f"Summary report {summary_path} does not exist."

    with open(summary_path, "r") as f:
        content = f.read().strip()

    expected_lines = [
        "Safe Extracted: 2",
        "Malicious Found: 2",
        "Recent Python Files: 2"
    ]

    for line in expected_lines:
        assert line in content, f"Expected line '{line}' not found in summary report."