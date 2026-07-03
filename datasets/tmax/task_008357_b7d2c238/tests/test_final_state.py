# test_final_state.py
import os
import subprocess
import pytest

REPORT_PATH = "/home/user/analysis_report.txt"
REPO_PATH = "/home/user/malware_analysis"

def get_deadlock_commit_hash():
    """Derive the expected commit hash from the git repository based on the commit message."""
    try:
        output = subprocess.check_output(
            ["git", "log", "--format=%H", "--grep=Add multithreading for faster processing"],
            cwd=REPO_PATH,
            text=True
        ).strip()
        return output.splitlines()[0] if output else None
    except Exception:
        return None

def test_analysis_report_exists():
    assert os.path.isfile(REPORT_PATH), f"Analysis report not found at {REPORT_PATH}."

def test_analysis_report_contents():
    assert os.path.isfile(REPORT_PATH), f"Analysis report not found at {REPORT_PATH}."

    with open(REPORT_PATH, "r") as f:
        lines = [line.strip() for line in f.read().strip().splitlines()]

    assert len(lines) >= 3, f"Analysis report must contain at least 3 lines, found {len(lines)}."

    # Line 1: Deadlock commit hash
    expected_hash = get_deadlock_commit_hash()
    assert expected_hash is not None, "Could not find the deadlock commit in the git repository to verify against."
    assert lines[0] == expected_hash, f"Line 1 incorrect. Expected commit hash {expected_hash}, got '{lines[0]}'."

    # Line 2: Hidden file path
    expected_path = "/home/user/.hidden_config_xyz_123.dat"
    assert lines[1] == expected_path, f"Line 2 incorrect. Expected '{expected_path}', got '{lines[1]}'."

    # Line 3: Decrypted payload
    expected_payload = "TOP_SECRET_EXFIL_DATA"
    assert lines[2] == expected_payload, f"Line 3 incorrect. Expected '{expected_payload}', got '{lines[2]}'."