# test_final_state.py

import os
import json
import urllib.request
import pytest

def test_flask_api_running():
    """Test that the Flask API is running on port 8000 and responds correctly."""
    url = "http://127.0.0.1:8000/energy"
    data = json.dumps({"graph": "0000000000"}).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode('utf-8'))
            assert "energy" in res, "API response missing 'energy' key."
            assert isinstance(res["energy"], (int, float)), "Energy value should be a number."
    except Exception as e:
        pytest.fail(f"Flask API is not running or failed to respond correctly: {e}")

def test_scripts_exist_and_executable():
    """Test that the required bash scripts exist and are executable."""
    scripts = [
        "/home/user/mcmc_sampler.sh",
        "/home/user/run_experiment.sh"
    ]
    for script in scripts:
        assert os.path.exists(script), f"Script missing: {script}"
        assert os.path.isfile(script), f"Not a file: {script}"
        assert os.access(script, os.X_OK), f"Script is not executable: {script}"

def test_log_files_exist_and_have_correct_length():
    """Test that the 3 chain log files exist, contain 500 lines each, and contain floats."""
    for i in range(1, 4):
        log_file = f"/home/user/chain_{i}.log"
        assert os.path.exists(log_file), f"Log file missing: {log_file}"

        with open(log_file, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]

        assert len(lines) == 500, f"{log_file} should contain exactly 500 lines, but has {len(lines)}."

        # Verify that all lines can be parsed as floats
        for idx, line in enumerate(lines):
            try:
                float(line)
            except ValueError:
                pytest.fail(f"Invalid float value in {log_file} at line {idx + 1}: '{line}'")

def test_convergence_result():
    """Test that convergence_result.txt exists and contains the correct average of the last 100 steps."""
    result_file = "/home/user/convergence_result.txt"
    assert os.path.exists(result_file), f"Result file missing: {result_file}"

    with open(result_file, 'r') as f:
        content = f.read().strip()

    try:
        reported_avg = float(content)
    except ValueError:
        pytest.fail(f"convergence_result.txt does not contain a valid float: '{content}'")

    # Calculate the expected average from the log files
    last_100_values = []
    for i in range(1, 4):
        log_file = f"/home/user/chain_{i}.log"
        with open(log_file, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
            last_100_values.extend([float(x) for x in lines[-100:]])

    assert len(last_100_values) == 300, "Should have exactly 300 values for the final average calculation."

    expected_avg = sum(last_100_values) / 300.0

    assert abs(reported_avg - expected_avg) < 1e-3, (
        f"Reported average {reported_avg} in {result_file} does not match "
        f"the expected calculated average {expected_avg}."
    )