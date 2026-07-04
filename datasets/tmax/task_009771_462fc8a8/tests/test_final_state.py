# test_final_state.py

import os
import json
import math
import subprocess
import pytest

def test_init_env_exists_and_executable():
    """Test that init_env.sh exists, is executable, and successfully sets up the environment."""
    script_path = "/home/user/init_env.sh"
    assert os.path.isfile(script_path), f"Missing setup script at {script_path}"
    assert os.access(script_path, os.X_OK), f"Setup script at {script_path} is not executable"

    # Verify idempotency and exit code
    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"{script_path} failed with exit code {result.returncode}. Stderr: {result.stderr}"

    # Check if directories and files were created
    assert os.path.isdir("/home/user/capacity_planner/data"), "/home/user/capacity_planner/data directory was not created"
    assert os.path.isfile("/home/user/capacity_planner/predictor/Cargo.toml"), "Cargo project was not initialized at /home/user/capacity_planner/predictor"

def test_clean_csv_exists_and_correct():
    """Test that clean.csv exists and contains the correctly formatted data."""
    csv_path = "/home/user/capacity_planner/data/clean.csv"
    assert os.path.isfile(csv_path), f"Missing cleaned CSV data at {csv_path}"

    with open(csv_path, "r") as f:
        lines = [line.strip() for line in f.read().splitlines() if line.strip()]

    expected_lines = [
        "node-alpha,50.0,2000.0",
        "node-beta,80.0,4000.0",
        "node-alpha,60.0,2400.0",
        "node-beta,90.0,4200.0"
    ]

    assert lines == expected_lines, f"Content of {csv_path} does not match expected output. Got: {lines}"

def test_report_json_exists_and_correct():
    """Test that report.json exists and contains the correct calculated averages and projections."""
    json_path = "/home/user/capacity_planner/report.json"
    assert os.path.isfile(json_path), f"Missing JSON report at {json_path}"

    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} does not contain valid JSON")

    assert "node-alpha" in data, "Missing 'node-alpha' in JSON report"
    assert "node-beta" in data, "Missing 'node-beta' in JSON report"

    alpha = data["node-alpha"]
    assert math.isclose(alpha.get("avg_cpu", 0), 55.0, rel_tol=1e-5), "node-alpha avg_cpu is incorrect"
    assert math.isclose(alpha.get("avg_mem", 0), 2200.0, rel_tol=1e-5), "node-alpha avg_mem is incorrect"
    assert math.isclose(alpha.get("projected_cpu", 0), 66.0, rel_tol=1e-5), "node-alpha projected_cpu is incorrect"
    assert math.isclose(alpha.get("projected_mem", 0), 2640.0, rel_tol=1e-5), "node-alpha projected_mem is incorrect"

    beta = data["node-beta"]
    assert math.isclose(beta.get("avg_cpu", 0), 85.0, rel_tol=1e-5), "node-beta avg_cpu is incorrect"
    assert math.isclose(beta.get("avg_mem", 0), 4100.0, rel_tol=1e-5), "node-beta avg_mem is incorrect"
    assert math.isclose(beta.get("projected_cpu", 0), 102.0, rel_tol=1e-5), "node-beta projected_cpu is incorrect"
    assert math.isclose(beta.get("projected_mem", 0), 4920.0, rel_tol=1e-5), "node-beta projected_mem is incorrect"