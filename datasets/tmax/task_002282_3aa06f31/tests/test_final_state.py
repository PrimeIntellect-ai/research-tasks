# test_final_state.py

import os
import subprocess
import pytest

BASE_DIR = "/home/user/sensor_net"
METRICS_LOG = os.path.join(BASE_DIR, "output", "metrics.log")
START_SCRIPT = os.path.join(BASE_DIR, "start.sh")
AGGREGATOR_PY = os.path.join(BASE_DIR, "aggregator.py")

def test_aggregator_modifications():
    """Verify the aggregator script contains logic to handle encoding and filtering."""
    assert os.path.isfile(AGGREGATOR_PY), f"File {AGGREGATOR_PY} is missing."
    with open(AGGREGATOR_PY, "r") as f:
        content = f.read()

    # Check for utf-16le handling
    assert "utf-16" in content.lower(), "aggregator.py does not appear to handle utf-16le encoding."

    # Check for boundary filtering logic (0.0 to 100.0)
    assert "100" in content, "aggregator.py does not appear to filter values > 100.0."
    assert "0" in content, "aggregator.py does not appear to filter values < 0.0."

def test_system_runs_stably():
    """Run the system for 10 seconds and verify it produces enough metrics without crashing."""
    if os.path.exists(METRICS_LOG):
        os.remove(METRICS_LOG)

    # Run the start script with a timeout of 10 seconds
    # `timeout` exits with 124 if the command times out, which is expected here.
    process = subprocess.run(
        ["timeout", "10", START_SCRIPT],
        cwd=BASE_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False
    )

    # If the script crashed before 10 seconds, the return code would likely be 1 or similar, not 124 or 0.
    assert process.returncode in (0, 124), f"start.sh exited prematurely with code {process.returncode}. Stderr: {process.stderr.decode()}"

    assert os.path.isfile(METRICS_LOG), f"Metrics log {METRICS_LOG} was not created."

    with open(METRICS_LOG, "r") as f:
        lines = f.readlines()

    assert len(lines) >= 5, f"Expected at least 5 lines in metrics.log, but found {len(lines)}."

    for line in lines:
        assert "StdDev" in line, f"Malformed line in metrics.log: {line.strip()}"