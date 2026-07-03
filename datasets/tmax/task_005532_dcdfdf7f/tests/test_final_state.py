# test_final_state.py

import os
import subprocess
import pytest

def test_run_pipeline_exists_and_executable():
    script_path = "/home/user/run_pipeline.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_pipeline_execution_and_artifacts():
    script_path = "/home/user/run_pipeline.sh"

    # Run the script
    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed to execute. Stderr: {result.stderr}"

    # Check bootstrap sample
    bootstrap_path = "/home/user/bootstrap_sample.csv"
    assert os.path.isfile(bootstrap_path), f"Bootstrap sample {bootstrap_path} was not created."

    with open(bootstrap_path, 'r') as f:
        lines = f.readlines()

    assert len(lines) == 50, f"Expected exactly 50 lines in bootstrap_sample.csv, found {len(lines)}."

    # Check if header is excluded (first line shouldn't be the header string)
    if lines:
        assert "col1,col2,col3,label" not in lines[0], "Bootstrap sample should not include the header."

    # Check final metric
    metric_path = "/home/user/final_metric.txt"
    assert os.path.isfile(metric_path), f"Final metric file {metric_path} was not created."

    with open(metric_path, 'r') as f:
        metric_content = f.read().strip()

    assert metric_content == "0.85", f"Expected final metric to be '0.85', but got '{metric_content}'."