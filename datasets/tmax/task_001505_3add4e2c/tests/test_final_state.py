# test_final_state.py
import subprocess
import re
import pytest

def test_evaluate_mse():
    """
    Runs the evaluation script and checks if the outputted FINAL_MSE is strictly less than 0.05.
    This verifies that the Rust service was successfully fixed, recompiled, and is running,
    and that the numerical instability has been resolved.
    """
    try:
        result = subprocess.run(
            ["python3", "/app/telemetry_system/evaluate.py"],
            capture_output=True,
            text=True,
            check=True
        )
        stdout = result.stdout
    except subprocess.CalledProcessError as e:
        pytest.fail(
            f"evaluate.py failed to run. Ensure the Rust service is running on port 8080 "
            f"and Redis is running on port 6379.\n"
            f"Exit code: {e.returncode}\n"
            f"stdout: {e.stdout}\n"
            f"stderr: {e.stderr}"
        )

    match = re.search(r"FINAL_MSE=([0-9eE.-]+)", stdout)
    if not match:
        pytest.fail(f"Could not find FINAL_MSE in evaluate.py output. Output was:\n{stdout}")

    mse = float(match.group(1))
    assert mse < 0.05, f"FINAL_MSE is {mse}, which is not strictly less than the threshold of 0.05"