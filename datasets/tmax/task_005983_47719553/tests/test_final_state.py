# test_final_state.py

import os
import subprocess

def test_pipeline_script_exists_and_executable():
    script_path = "/home/user/prepare_pipeline.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_pipeline_script_environment_variables():
    script_path = "/home/user/prepare_pipeline.sh"
    with open(script_path, "r") as f:
        content = f.read()
    assert "OPENBLAS_NUM_THREADS=1" in content, "OPENBLAS_NUM_THREADS=1 not found in script."
    assert "PYTHONHASHSEED=0" in content, "PYTHONHASHSEED=0 not found in script."

def test_pipeline_execution_and_outputs():
    script_path = "/home/user/prepare_pipeline.sh"

    # Run the script
    result = subprocess.run(["bash", script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script execution failed with return code {result.returncode}.\nStderr: {result.stderr}"

    # Check joined.csv
    joined_path = "/home/user/joined.csv"
    assert os.path.isfile(joined_path), f"File {joined_path} was not created by the script."

    with open(joined_path, "r") as f:
        joined_content = f.read().strip()

    expected_joined = (
        "1,25,US,100,5\n"
        "2,30,UK,150,10\n"
        "3,22,US,200,2\n"
        "4,35,CA,50,0\n"
        "5,28,UK,120,8"
    )

    # Compare lines to be robust against trailing newlines
    assert joined_content.splitlines() == expected_joined.splitlines(), f"Content of {joined_path} is incorrect."

    # Check ci_results.txt
    ci_path = "/home/user/ci_results.txt"
    assert os.path.isfile(ci_path), f"File {ci_path} was not created by the script."

    with open(ci_path, "r") as f:
        ci_content = f.read().strip()

    expected_ci = "74.96,173.04"
    assert ci_content == expected_ci, f"Content of {ci_path} is incorrect. Expected '{expected_ci}', got '{ci_content}'."