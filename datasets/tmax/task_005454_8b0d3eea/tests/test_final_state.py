# test_final_state.py

import os
import subprocess
import pytest

def test_pipeline_output():
    script_path = "/home/user/pipeline.py"

    # Ensure the script exists
    assert os.path.exists(script_path), f"Script missing at {script_path}"
    assert os.path.isfile(script_path), f"{script_path} is not a file"

    # Run the script
    try:
        result = subprocess.run(
            ["python3", script_path],
            capture_output=True,
            text=True,
            timeout=300
        )
    except subprocess.TimeoutExpired:
        pytest.fail("The script took longer than 300 seconds to execute.")

    assert result.returncode == 0, f"Script failed with return code {result.returncode}. Stderr: {result.stderr}"

    stdout_str = result.stdout.strip()

    # Parse output as float
    try:
        agent_value = float(stdout_str)
    except ValueError:
        pytest.fail(f"Script output could not be parsed as a float. Output was: {stdout_str!r}")

    # Ground truth values
    actual_distance = 145.5
    shortest_distance = 82.0
    expected_value = shortest_distance / actual_distance

    # Calculate metric
    error = abs(agent_value - expected_value)

    # Assert threshold
    assert error <= 0.05, f"Output {agent_value} is not within 0.05 of expected value {expected_value:.5f} (Error: {error:.5f})"