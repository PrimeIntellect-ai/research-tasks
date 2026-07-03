# test_final_state.py

import os
import json
import subprocess
import pytest

def test_logrotate_config_valid():
    """
    Verify that the logrotate config exists and has valid syntax.
    """
    conf_path = "/app/logrotate.conf"
    assert os.path.exists(conf_path), f"Logrotate config not found at {conf_path}"

    # Check syntax using logrotate debug mode
    cmd = ["logrotate", "-d", "-s", "/app/logs/logrotate.status", conf_path]
    result = subprocess.run(cmd, capture_output=True, text=True)

    assert result.returncode == 0, (
        f"logrotate syntax check failed for {conf_path}.\n"
        f"Return code: {result.returncode}\n"
        f"STDOUT:\n{result.stdout}\n"
        f"STDERR:\n{result.stderr}"
    )

def test_benchmark_success_rate():
    """
    Verify that the benchmark results exist, are valid JSON, 
    and the success_rate metric meets the threshold.
    """
    results_path = "/app/benchmark_results.json"
    assert os.path.exists(results_path), f"Benchmark results file not found at {results_path}"

    with open(results_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Failed to parse {results_path} as JSON: {e}")

    assert "success_rate" in data, f"'success_rate' key missing in {results_path}"

    try:
        success_rate = float(data["success_rate"])
    except ValueError:
        pytest.fail(f"'success_rate' is not a valid float: {data['success_rate']}")

    threshold = 0.95
    assert success_rate >= threshold, (
        f"Benchmark success_rate {success_rate} is below the required threshold of {threshold}. "
        "This indicates Nginx, the SSH tunnel, or the backend are not functioning correctly."
    )