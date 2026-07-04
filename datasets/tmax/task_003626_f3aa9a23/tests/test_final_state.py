# test_final_state.py

import os
import subprocess
import statistics
import tempfile
import pytest

def test_recovered_latency_log_exists():
    path = "/home/user/recovered_latency.log"
    assert os.path.exists(path), f"File {path} is missing."
    assert os.path.isfile(path), f"Path {path} is not a file."

def test_stable_variance_script_accuracy():
    script_path = "/home/user/stable_variance.sh"
    assert os.path.exists(script_path), f"Script {script_path} is missing."
    assert os.access(script_path, os.X_OK) or os.path.isfile(script_path), f"{script_path} must be a file."

    # Generate hidden test data
    test_data = [
        5000000.001,
        5000000.002,
        5000000.003,
        5000000.005,
        5000000.008,
        5000000.013,
        5000000.021,
    ]
    true_variance = statistics.variance(test_data)

    with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp:
        for val in test_data:
            tmp.write(f"{val}\n")
        tmp_path = tmp.name

    try:
        result = subprocess.run(
            ["bash", script_path, tmp_path],
            capture_output=True,
            text=True,
            check=False
        )
        assert result.returncode == 0, f"{script_path} failed with return code {result.returncode} and stderr: {result.stderr}"

        output = result.stdout.strip()
        try:
            agent_variance = float(output)
        except ValueError:
            pytest.fail(f"Could not parse float from script output: '{output}'")

        error = abs(agent_variance - true_variance)
        assert error < 0.001, f"Absolute error {error} is >= 0.001. Agent output: {agent_variance}, True variance: {true_variance}"
    finally:
        os.remove(tmp_path)

def test_regression_script_exists_and_succeeds():
    script_path = "/home/user/regression.sh"
    assert os.path.exists(script_path), f"Script {script_path} is missing."

    result = subprocess.run(
        ["bash", script_path],
        capture_output=True,
        text=True,
        check=False
    )
    assert result.returncode == 0, f"{script_path} failed with return code {result.returncode} and stderr: {result.stderr}"