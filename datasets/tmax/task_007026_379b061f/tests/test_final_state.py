# test_final_state.py
import os
import json
import subprocess
import pytest

APP_DIR = "/home/user/app"
REPORT_PATH = "/home/user/report.json"
TEST_SCRIPT_PATH = "/home/user/test_race.py"

def get_expected_commit_hash():
    try:
        result = subprocess.run(
            ["git", "log", "--grep=Optimize cache updates", "--format=%H"],
            cwd=APP_DIR,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None

def test_report_json():
    assert os.path.isfile(REPORT_PATH), f"Report file not found at {REPORT_PATH}"

    with open(REPORT_PATH, "r") as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("report.json is not valid JSON")

    expected_api_key = "sk-live-99a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4"
    expected_hash = get_expected_commit_hash()

    assert report.get("leaked_api_key") == expected_api_key, "Incorrect leaked_api_key in report.json"
    assert report.get("leak_commit_hash") == expected_hash, "Incorrect leak_commit_hash in report.json"

def test_regression_script_behavior():
    assert os.path.isfile(TEST_SCRIPT_PATH), f"Regression test script not found at {TEST_SCRIPT_PATH}"

    # Ensure we are on the buggy commit (HEAD)
    subprocess.run(["git", "checkout", "master"], cwd=APP_DIR, capture_output=True)

    # Run script on buggy code
    result_buggy = subprocess.run(
        ["python3", TEST_SCRIPT_PATH],
        cwd=APP_DIR,
        capture_output=True
    )
    assert result_buggy.returncode == 1, "test_race.py should exit with code 1 when the race condition is present"

    # Checkout previous commit (safe code)
    try:
        subprocess.run(["git", "checkout", "HEAD~1"], cwd=APP_DIR, capture_output=True, check=True)

        # Run script on safe code
        result_safe = subprocess.run(
            ["python3", TEST_SCRIPT_PATH],
            cwd=APP_DIR,
            capture_output=True
        )
        assert result_safe.returncode == 0, "test_race.py should exit with code 0 when the race condition is NOT present"
    finally:
        # Restore git state
        subprocess.run(["git", "checkout", "-"], cwd=APP_DIR, capture_output=True)