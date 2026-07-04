# test_final_state.py
import os
import json
import subprocess
import pytest

WORKSPACE = "/home/user/workspace"
SOLVER_C = os.path.join(WORKSPACE, "solver.c")
PIPELINE_NB = os.path.join(WORKSPACE, "pipeline.ipynb")
RUN_SCRIPT = os.path.join(WORKSPACE, "run_pipeline.sh")
SOLVER_BIN = os.path.join(WORKSPACE, "solver")
RESULTS_JSON = os.path.join(WORKSPACE, "results.json")

def test_files_exist():
    assert os.path.isfile(SOLVER_C), f"Expected C program {SOLVER_C} to exist."
    assert os.path.isfile(PIPELINE_NB), f"Expected Jupyter notebook {PIPELINE_NB} to exist."
    assert os.path.isfile(RUN_SCRIPT), f"Expected bash script {RUN_SCRIPT} to exist."

def test_script_executable():
    assert os.access(RUN_SCRIPT, os.X_OK), f"Expected {RUN_SCRIPT} to be executable."

def test_pipeline_execution():
    # Clean up artifacts if they exist to ensure the script actually builds/runs them
    if os.path.exists(SOLVER_BIN):
        os.remove(SOLVER_BIN)
    if os.path.exists(RESULTS_JSON):
        os.remove(RESULTS_JSON)

    # Run the bash script
    try:
        result = subprocess.run(
            [RUN_SCRIPT],
            cwd=WORKSPACE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"{RUN_SCRIPT} failed to execute properly.\nSTDOUT: {e.stdout}\nSTDERR: {e.stderr}")

    # Verify artifacts were created
    assert os.path.isfile(SOLVER_BIN), f"Expected {SOLVER_BIN} to be compiled and exist after running the script."
    assert os.path.isfile(RESULTS_JSON), f"Expected {RESULTS_JSON} to be created after running the script."

    # Read and verify results
    with open(RESULTS_JSON, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{RESULTS_JSON} is not a valid JSON file.")

    assert "x0" in data, "JSON result is missing key 'x0'"
    assert "x1" in data, "JSON result is missing key 'x1'"

    x0 = float(data["x0"])
    x1 = float(data["x1"])

    expected_x0 = 0.598802
    expected_x1 = 1.197605

    assert abs(x0 - expected_x0) < 1e-4, f"Expected x0 to be near {expected_x0}, but got {x0}"
    assert abs(x1 - expected_x1) < 1e-4, f"Expected x1 to be near {expected_x1}, but got {x1}"