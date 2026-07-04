# test_final_state.py

import os
import subprocess
import pytest

WORKSPACE = '/home/user/workspace'
RESULTS_FILE = '/home/user/results.csv'

def test_workspace_and_files_exist():
    assert os.path.isdir(WORKSPACE), f"Workspace directory {WORKSPACE} is missing."
    assert os.path.isfile(os.path.join(WORKSPACE, 'fit_models.c')), "fit_models.c is missing in workspace."
    assert os.path.isfile(os.path.join(WORKSPACE, 'Makefile')), "Makefile is missing in workspace."
    assert os.path.isfile(os.path.join(WORKSPACE, 'run_pipeline.sh')), "run_pipeline.sh is missing in workspace."

def test_run_pipeline():
    script_path = os.path.join(WORKSPACE, 'run_pipeline.sh')

    # Remove results file if it exists to ensure the script creates it
    if os.path.exists(RESULTS_FILE):
        os.remove(RESULTS_FILE)

    result = subprocess.run(['bash', script_path], cwd=WORKSPACE, capture_output=True, text=True)
    assert result.returncode == 0, f"run_pipeline.sh failed with return code {result.returncode}.\nStderr: {result.stderr}\nStdout: {result.stdout}"

def test_results_csv_content():
    assert os.path.isfile(RESULTS_FILE), f"{RESULTS_FILE} was not created by the pipeline."

    with open(RESULTS_FILE, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 lines of output in {RESULTS_FILE}, got {len(lines)}."

    # Validate Dataset 1
    parts1 = lines[0].split(',')
    assert len(parts1) == 3, f"Line 1 invalid format. Expected 3 comma-separated values, got: {lines[0]}"
    assert parts1[0] == 'dataset_1', f"Line 1 expected dataset_name 'dataset_1', got '{parts1[0]}'"
    assert parts1[1] == 'Normal', f"Line 1 expected Best_Model 'Normal', got '{parts1[1]}'"
    try:
        diff1 = float(parts1[2])
        assert abs(diff1 - 268.0435) <= 0.0002, f"Line 1 Log_Likelihood_Difference expected ~268.0435, got {diff1}"
    except ValueError:
        pytest.fail(f"Line 1 Log_Likelihood_Difference is not a valid float: {parts1[2]}")

    # Validate Dataset 2
    parts2 = lines[1].split(',')
    assert len(parts2) == 3, f"Line 2 invalid format. Expected 3 comma-separated values, got: {lines[1]}"
    assert parts2[0] == 'dataset_2', f"Line 2 expected dataset_name 'dataset_2', got '{parts2[0]}'"
    assert parts2[1] == 'Laplace', f"Line 2 expected Best_Model 'Laplace', got '{parts2[1]}'"
    try:
        diff2 = float(parts2[2])
        assert abs(diff2 - 492.2030) <= 0.0002, f"Line 2 Log_Likelihood_Difference expected ~492.2030, got {diff2}"
    except ValueError:
        pytest.fail(f"Line 2 Log_Likelihood_Difference is not a valid float: {parts2[2]}")