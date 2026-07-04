# test_final_state.py

import os
import subprocess
import math

def test_files_exist():
    """Verify that the required source file and bash script exist."""
    assert os.path.isfile("/home/user/prepare_data.cpp"), "/home/user/prepare_data.cpp does not exist."
    assert os.path.isfile("/home/user/run.sh"), "/home/user/run.sh does not exist."

def test_run_script_and_validate_output():
    """Run the bash script and validate the output in validation.log."""
    # Ensure the script is executable or run it with bash
    result = subprocess.run(["bash", "/home/user/run.sh"], capture_output=True, text=True)
    assert result.returncode == 0, f"run.sh failed to execute. stderr: {result.stderr}"

    log_path = "/home/user/validation.log"
    assert os.path.isfile(log_path), f"{log_path} was not created by the script."

    with open(log_path, "r") as f:
        content = f.read().strip()

    try:
        actual_value = float(content)
    except ValueError:
        assert False, f"Output in {log_path} is not a valid float. Got: '{content}'"

    expected_value = 63.245553
    tolerance = 1e-4

    assert abs(actual_value - expected_value) < tolerance, (
        f"The computed L2 norm is incorrect. "
        f"Expected approximately {expected_value}, but got {actual_value}."
    )