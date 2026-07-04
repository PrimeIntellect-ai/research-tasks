# test_final_state.py
import os
import subprocess
import pytest

def test_get_metric_script():
    script_path = "/home/user/build/get_metric.sh"

    assert os.path.isfile(script_path), f"The target script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"The script {script_path} is not executable."

    try:
        result = subprocess.run([script_path], capture_output=True, text=True, check=True, timeout=15)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Execution of {script_path} failed with return code {e.returncode}. Stderr: {e.stderr}")
    except subprocess.TimeoutExpired:
        pytest.fail(f"Execution of {script_path} timed out.")

    output = result.stdout.strip()

    try:
        agent_val = float(output)
    except ValueError:
        pytest.fail(f"Output from {script_path} is not a valid float. Got: {output!r}")

    target_val = 142.6
    relative_error = abs((agent_val - target_val) / target_val)

    assert relative_error <= 0.05, (
        f"Relative error {relative_error:.4f} exceeds tolerance 0.05. "
        f"Agent output: {agent_val}, Target: {target_val}"
    )