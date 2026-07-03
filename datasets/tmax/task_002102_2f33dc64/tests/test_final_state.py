# test_final_state.py

import os
import json
import time
import subprocess
import pytest

SCRIPT_PATH = "/home/user/fast_etl.py"
OUTPUT_PATH = "/home/user/summary.json"

def test_script_exists():
    """Verify that the fast_etl.py script exists."""
    assert os.path.exists(SCRIPT_PATH), f"Expected script not found at {SCRIPT_PATH}"
    assert os.path.isfile(SCRIPT_PATH), f"Path {SCRIPT_PATH} is not a file"

def test_execution_time_and_correctness():
    """Run the script, check execution time, and validate the output."""
    # Ensure any previous output is removed to guarantee we test the new run
    if os.path.exists(OUTPUT_PATH):
        os.remove(OUTPUT_PATH)

    start_time = time.time()
    try:
        result = subprocess.run(
            ["python", SCRIPT_PATH],
            capture_output=True,
            text=True,
            timeout=15,
            check=True
        )
    except subprocess.TimeoutExpired:
        pytest.fail(f"Script execution timed out after 15 seconds.")
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Script execution failed with exit code {e.returncode}.\nStdout: {e.stdout}\nStderr: {e.stderr}")

    runtime = time.time() - start_time

    # Validate output exists
    assert os.path.exists(OUTPUT_PATH), f"Output file not found at {OUTPUT_PATH}"

    # Validate correctness
    with open(OUTPUT_PATH, 'r') as f:
        try:
            summary = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Output file {OUTPUT_PATH} is not valid JSON.")

    expected_amount = 45210.50
    expected_token = "urgent"

    assert "total_amount" in summary, "Key 'total_amount' missing in output JSON."
    assert "top_token" in summary, "Key 'top_token' missing in output JSON."

    actual_amount = summary.get("total_amount")
    actual_token = summary.get("top_token")

    assert isinstance(actual_amount, (int, float)), f"'total_amount' must be a number, got {type(actual_amount)}"
    assert abs(actual_amount - expected_amount) <= 0.1, f"Incorrect total_amount. Expected ~{expected_amount}, got {actual_amount}"

    assert actual_token == expected_token, f"Incorrect top_token. Expected '{expected_token}', got '{actual_token}'"

    # Validate performance
    assert runtime <= 2.0, f"Performance requirement failed: execution took {runtime:.2f} seconds, threshold is <= 2.0 seconds."