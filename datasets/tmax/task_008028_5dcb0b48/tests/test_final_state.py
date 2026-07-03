# test_final_state.py

import os
import json
import subprocess
import pytest

PROJECT_DIR = "/home/user/project"
SECRET_FILE = "/home/user/secret.txt"
SUMMARY_FILE = os.path.join(PROJECT_DIR, "summary.json")
BUILD_SCRIPT = os.path.join(PROJECT_DIR, "build.sh")

def test_secret_recovered():
    assert os.path.isfile(SECRET_FILE), f"Secret file {SECRET_FILE} is missing."
    with open(SECRET_FILE, "r") as f:
        content = f.read().strip()
    assert content == "S3cr3t_P4ssW0rd_992!", f"Secret file contains incorrect content: {content}"

def test_summary_json_is_correct():
    assert os.path.isfile(SUMMARY_FILE), f"Summary file {SUMMARY_FILE} is missing."
    with open(SUMMARY_FILE, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("summary.json is not valid JSON.")

    assert "total_sum" in data, "summary.json is missing 'total_sum' key."
    assert data["total_sum"] == 150, f"Expected total_sum to be 150, but got {data['total_sum']}."

def test_build_script_runs_successfully_and_safely():
    # Run the build script to ensure it handles spaces and race conditions correctly
    try:
        result = subprocess.run(
            ["bash", BUILD_SCRIPT],
            cwd=PROJECT_DIR,
            capture_output=True,
            text=True,
            timeout=10
        )
        assert result.returncode == 0, f"build.sh failed with exit code {result.returncode}. stderr: {result.stderr}"
    except subprocess.TimeoutExpired:
        pytest.fail("build.sh timed out. Make sure it waits for background processes correctly without hanging.")

    # Check the summary again after our run
    assert os.path.isfile(SUMMARY_FILE), f"Summary file {SUMMARY_FILE} is missing after running build.sh."
    with open(SUMMARY_FILE, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("summary.json is not valid JSON after running build.sh.")

    assert "total_sum" in data, "summary.json is missing 'total_sum' key after running build.sh."
    assert data["total_sum"] == 150, f"Expected total_sum to be 150 after running build.sh, but got {data['total_sum']}. Race condition or file space issue might still exist."