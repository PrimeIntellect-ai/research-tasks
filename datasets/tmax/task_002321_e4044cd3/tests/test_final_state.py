# test_final_state.py

import os
import subprocess
import math
import pytest

SCRIPT_PATH = "/home/user/orchestrate_pipeline.sh"
RAW_SCORES_PATH = "/home/user/raw_scores.txt"
CALC_VAR_PATH = "/home/user/calculated_variance.txt"
REF_VAR_PATH = "/home/user/reference_variance.txt"
STATUS_LOG_PATH = "/home/user/pipeline_status.log"

def test_orchestrator_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script {SCRIPT_PATH} is not executable."

def test_orchestrator_execution_and_outputs():
    # Remove outputs if they exist to ensure the script generates them
    for path in [RAW_SCORES_PATH, CALC_VAR_PATH, STATUS_LOG_PATH]:
        if os.path.exists(path):
            os.remove(path)

    # Run the orchestrator script
    result = subprocess.run([SCRIPT_PATH], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed to execute. stderr: {result.stderr}"

    # Verify raw scores were generated
    assert os.path.isfile(RAW_SCORES_PATH), f"{RAW_SCORES_PATH} was not created by the notebook."

    with open(RAW_SCORES_PATH, 'r') as f:
        scores = [float(line.strip()) for line in f if line.strip()]

    assert len(scores) > 0, "No scores found in raw_scores.txt"

    # Calculate expected population variance in Python (numerically stable by default for these sizes)
    n = len(scores)
    mean = sum(scores) / n
    expected_variance = sum((x - mean) ** 2 for x in scores) / n

    # Verify calculated variance file
    assert os.path.isfile(CALC_VAR_PATH), f"{CALC_VAR_PATH} was not created."
    with open(CALC_VAR_PATH, 'r') as f:
        calc_var_str = f.read().strip()

    try:
        calc_var = float(calc_var_str)
    except ValueError:
        pytest.fail(f"Calculated variance is not a valid float: {calc_var_str}")

    # The calculated variance should match our expected variance closely
    assert math.isclose(calc_var, expected_variance, rel_tol=1e-5, abs_tol=1e-6), \
        f"Calculated variance {calc_var} does not match expected {expected_variance}"

    # Check formatting (6 decimal places)
    assert len(calc_var_str.split('.')[-1]) == 6, f"Variance {calc_var_str} is not formatted to 6 decimal places."

    # Verify pipeline status log
    assert os.path.isfile(REF_VAR_PATH), f"Reference variance file {REF_VAR_PATH} is missing."
    with open(REF_VAR_PATH, 'r') as f:
        ref_var = float(f.read().strip())

    expected_status = "PASS" if abs(calc_var - ref_var) < 0.0001 else "FAIL"

    assert os.path.isfile(STATUS_LOG_PATH), f"{STATUS_LOG_PATH} was not created."
    with open(STATUS_LOG_PATH, 'r') as f:
        status = f.read().strip()

    assert status == expected_status, f"Expected status '{expected_status}', but got '{status}' in {STATUS_LOG_PATH}"