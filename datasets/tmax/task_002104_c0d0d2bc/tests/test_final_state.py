# test_final_state.py

import os
import subprocess
import pytest

def test_pipeline_exists_and_executable():
    pipeline_path = "/home/user/pipeline.sh"
    assert os.path.isfile(pipeline_path), f"{pipeline_path} does not exist."
    assert os.access(pipeline_path, os.X_OK), f"{pipeline_path} is not executable."

def test_c_source_exists():
    c_path = "/home/user/classifier.c"
    assert os.path.isfile(c_path), f"{c_path} does not exist."

def test_pipeline_execution_and_results():
    pipeline_path = "/home/user/pipeline.sh"
    results_path = "/home/user/results.csv"

    # Remove results.csv if it exists to ensure the pipeline actually creates it
    if os.path.exists(results_path):
        os.remove(results_path)

    # Run the pipeline
    try:
        subprocess.run([pipeline_path], check=True, cwd="/home/user", capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Execution of {pipeline_path} failed.\nStdout: {e.stdout}\nStderr: {e.stderr}")

    assert os.path.isfile(results_path), f"{results_path} was not created by the pipeline."

    with open(results_path, "r") as f:
        content = [line.strip() for line in f.read().strip().splitlines() if line.strip()]

    expected = [
        "id,class",
        "1,1",
        "2,0",
        "3,1",
        "4,0",
        "6,1",
        "7,0"
    ]

    assert content == expected, f"Content of {results_path} does not match expected output.\nExpected: {expected}\nGot: {content}"