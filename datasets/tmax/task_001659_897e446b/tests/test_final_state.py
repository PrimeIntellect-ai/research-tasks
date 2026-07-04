# test_final_state.py

import os
import time
import subprocess
import pytest

def test_fstab_entry():
    """Verify that the fstab entry was correctly extracted and saved."""
    fstab_path = "/app/fstab_entry.txt"
    assert os.path.exists(fstab_path), f"{fstab_path} is missing"

    with open(fstab_path, "r") as f:
        content = f.read().strip()

    expected_entry = "tmpfs /app/run tmpfs rw,nosuid,nodev,size=50m 0 0"
    assert expected_entry in content, f"Incorrect fstab entry. Expected to find '{expected_entry}' in {fstab_path}"

def test_pipeline_execution_time():
    """Verify that the pipeline script exists, runs successfully, and completes within the performance threshold."""
    pipeline_path = "/app/pipeline.sh"
    assert os.path.exists(pipeline_path), f"{pipeline_path} is missing"
    assert os.access(pipeline_path, os.X_OK), f"{pipeline_path} is not executable"

    start_time = time.time()
    result = subprocess.run(["bash", pipeline_path], capture_output=True, text=True)
    end_time = time.time()

    runtime = end_time - start_time

    assert result.returncode == 0, f"pipeline.sh failed with return code {result.returncode}. stderr: {result.stderr}"

    threshold = 0.5
    assert runtime <= threshold, f"Execution time {runtime:.4f}s exceeds the {threshold}s threshold. The exporter bottleneck might not be fully removed."