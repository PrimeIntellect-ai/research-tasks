# test_final_state.py

import json
import os
import subprocess
import pytest

def test_systemd_service_active():
    """Verify that the systemd user service is running."""
    # We need to set XDG_RUNTIME_DIR to run systemctl --user in tests if it's not set,
    # but usually the test runner environment handles this. We will just call it.
    env = os.environ.copy()
    if 'XDG_RUNTIME_DIR' not in env:
        env['XDG_RUNTIME_DIR'] = f"/run/user/{os.getuid()}"

    result = subprocess.run(
        ["systemctl", "--user", "is-active", "local-proxy.service"],
        capture_output=True,
        text=True,
        env=env
    )
    status = result.stdout.strip()
    assert result.returncode == 0, f"local-proxy.service is not active. Current status: '{status}'"

def test_benchmark_results_metric():
    """Verify the benchmark results meet the required metric threshold."""
    results_path = '/home/user/bench_results.json'
    assert os.path.exists(results_path), f"Output file {results_path} not found. Ensure you saved the benchmark output."

    try:
        with open(results_path, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"File {results_path} does not contain valid JSON.")

    unique_backends = data.get('unique_backends', 0)
    errors = data.get('errors', -1)
    rps = data.get('rps', 0.0)

    # The proxy must successfully distribute traffic to all 3 backends without errors
    assert unique_backends == 3, f"Expected traffic to be distributed across 3 unique backends, but got {unique_backends}."
    assert errors == 0, f"Expected 0 errors during benchmark, but got {errors}."

    metric = float(rps)
    threshold = 100.0

    assert metric >= threshold, f"Benchmark RPS {metric} is below the required threshold of {threshold}."