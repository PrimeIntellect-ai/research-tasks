# test_final_state.py

import os
import json
import subprocess
import pytest

def test_script_exists_and_executable():
    script_path = "/home/user/ci_benchmark.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_script_execution_and_artifact():
    script_path = "/home/user/ci_benchmark.sh"
    artifact_path = "/home/user/artifacts/bench_results.json"

    # Remove artifact if it exists to ensure the script creates a new one
    if os.path.exists(artifact_path):
        os.remove(artifact_path)

    # Run the script
    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed to execute. stdout: {result.stdout}\nstderr: {result.stderr}"

    # Verify artifact existence
    assert os.path.isfile(artifact_path), f"Artifact {artifact_path} was not created by the script."

    # Verify JSON content
    with open(artifact_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Artifact {artifact_path} does not contain valid JSON.")

    assert "user_time_seconds" in data, "JSON missing key: 'user_time_seconds'"
    assert "max_rss_kb" in data, "JSON missing key: 'max_rss_kb'"

    assert isinstance(data["user_time_seconds"], (int, float)), "'user_time_seconds' must be a number (float or int)."
    assert isinstance(data["max_rss_kb"], int), "'max_rss_kb' must be an integer."