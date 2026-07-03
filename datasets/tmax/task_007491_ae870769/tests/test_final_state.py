# test_final_state.py

import os
import subprocess
import pytest

def test_pipeline_sh_executable():
    path = "/home/user/pipeline.sh"
    assert os.path.isfile(path), f"Missing required file: {path}"
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_pipeline_execution_and_metrics():
    path = "/home/user/pipeline.sh"
    metrics_path = "/home/user/metrics.txt"

    # Remove metrics.txt if it exists to ensure the script creates it
    if os.path.exists(metrics_path):
        os.remove(metrics_path)

    # Run the pipeline script
    result = subprocess.run([path], capture_output=True, text=True, cwd="/home/user")
    assert result.returncode == 0, f"pipeline.sh failed to execute with return code {result.returncode}.\nstdout: {result.stdout}\nstderr: {result.stderr}"

    assert os.path.isfile(metrics_path), f"File {metrics_path} was not created by pipeline.sh."

    with open(metrics_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 lines in metrics.txt, found {len(lines)}."

    # Check first line (gprof time)
    try:
        gprof_time = float(lines[0])
    except ValueError:
        pytest.fail(f"First line of metrics.txt is not a valid number: '{lines[0]}'")

    assert 50.0 <= gprof_time <= 100.0, f"Expected % time in refine_mesh to be between 50.0 and 100.0, got {gprof_time}."

    # Check second line (KDE max density)
    try:
        kde_max = float(lines[1])
    except ValueError:
        pytest.fail(f"Second line of metrics.txt is not a valid number: '{lines[1]}'")

    assert 0.060 <= kde_max <= 0.063, f"Expected KDE max density to be around 0.0617, got {kde_max}."