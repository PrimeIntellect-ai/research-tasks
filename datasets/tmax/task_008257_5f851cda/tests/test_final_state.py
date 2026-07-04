# test_final_state.py

import os
import subprocess

PROJECT_DIR = "/home/user/rust_project"
SUCCESS_FILE = "/home/user/success.txt"
ENV_FILE = os.path.join(PROJECT_DIR, ".env")
EXPECTED_TOKEN = "rust_sec_77b31x"

def test_success_file():
    assert os.path.isfile(SUCCESS_FILE), f"Success file {SUCCESS_FILE} is missing."
    with open(SUCCESS_FILE, "r") as f:
        lines = f.read().strip().splitlines()

    assert len(lines) == 2, f"Expected exactly 2 lines in {SUCCESS_FILE}, but found {len(lines)}."
    assert lines[0] == EXPECTED_TOKEN, f"Line 1 of {SUCCESS_FILE} is incorrect. Expected '{EXPECTED_TOKEN}', got '{lines[0]}'."
    assert lines[1] == "TESTS_PASSED", f"Line 2 of {SUCCESS_FILE} is incorrect. Expected 'TESTS_PASSED', got '{lines[1]}'."

def test_env_file_restored():
    assert os.path.isfile(ENV_FILE), f".env file missing at {ENV_FILE}"
    with open(ENV_FILE, "r") as f:
        content = f.read()

    expected_line = f"SECRET_TOKEN={EXPECTED_TOKEN}"
    assert expected_line in content, f".env file does not contain the correct secret token. Expected '{expected_line}'."

def test_cargo_test_passes():
    # Run cargo test to ensure all tests pass (which verifies the race condition and precision fixes)
    result = subprocess.run(
        ["cargo", "test"],
        cwd=PROJECT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    assert result.returncode == 0, f"cargo test failed.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

def test_analytics_precision_fix():
    # Verify that analytics.rs contains f64 to fix the precision issue
    analytics_file = os.path.join(PROJECT_DIR, "src", "analytics.rs")
    assert os.path.isfile(analytics_file), f"Source file {analytics_file} is missing."
    with open(analytics_file, "r") as f:
        content = f.read()

    # We expect f64 to be used for the accumulation
    assert "f64" in content, "The analytics.rs file does not appear to use f64 for accumulation as requested."