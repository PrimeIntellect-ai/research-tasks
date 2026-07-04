# test_final_state.py

import os
import json
import pytest

def test_directories_and_symlink():
    """Test that the required directories and symlink are created."""
    assert os.path.isdir("/home/user/services/logs"), "/home/user/services/logs directory is missing"
    assert os.path.isdir("/home/user/services/run"), "/home/user/services/run directory is missing"

    symlink_path = "/home/user/logs"
    assert os.path.islink(symlink_path), f"{symlink_path} is not a symlink"

    target = os.readlink(symlink_path)
    # Handle both absolute and relative symlinks correctly
    if not os.path.isabs(target):
        target = os.path.normpath(os.path.join(os.path.dirname(symlink_path), target))
    assert target == "/home/user/services/logs", f"Symlink {symlink_path} does not point to /home/user/services/logs"

def test_scripts_exist():
    """Test that the automation and proxy scripts exist."""
    assert os.path.isfile("/home/user/start_backends.py"), "/home/user/start_backends.py is missing"
    assert os.path.isfile("/home/user/proxy.py"), "/home/user/proxy.py is missing"

def test_perturbation_removed():
    """Test that the blocking sleep perturbation was removed or commented out."""
    client_py_path = "/app/vendored/netprobe-1.0.0/netprobe/client.py"
    assert os.path.isfile(client_py_path), f"client.py missing: {client_py_path}"

    with open(client_py_path, "r") as f:
        content = f.read()

    for line in content.splitlines():
        if "time.sleep(0.1)" in line:
            assert line.lstrip().startswith("#"), "The blocking 'time.sleep(0.1)' is still present and not commented out in client.py"

def test_metric_threshold():
    """Test that the system achieved the required RPS threshold."""
    results_path = "/home/user/probe_results.json"
    assert os.path.isfile(results_path), f"Results file missing: {results_path}. The load test was not run or didn't save output."

    try:
        with open(results_path, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"Results file {results_path} is not valid JSON.")

    rps = float(data.get("requests_per_second", 0))
    assert rps >= 200.0, f"RPS metric threshold not met. Expected >= 200.0, got {rps}"