# test_final_state.py

import subprocess
import json
import os
import pytest

def test_traffic_gen_success_rate():
    """
    Run the adversarial traffic generator against the agent's proxy and operator,
    and verify that the success rate is at least 0.95.
    """
    binary_path = "/app/traffic_gen"
    assert os.path.isfile(binary_path), f"Traffic generator binary not found at {binary_path}"
    assert os.access(binary_path, os.X_OK), f"Traffic generator binary at {binary_path} is not executable"

    target_url = "http://127.0.0.1:8080"

    # Run the traffic generator
    res = subprocess.run(
        [binary_path, "--target", target_url], 
        capture_output=True, 
        text=True
    )

    try:
        # The generator should output a JSON blob on its last line
        lines = [line.strip() for line in res.stdout.splitlines() if line.strip()]
        assert len(lines) > 0, "Traffic generator produced no stdout."

        output = json.loads(lines[-1])
        rate = float(output["success_rate"])

        assert rate >= 0.95, f"Success rate {rate} is below the required threshold of 0.95"
    except Exception as e:
        raise AssertionError(f"Verification failed: {e}\nStdout: {res.stdout}\nStderr: {res.stderr}")