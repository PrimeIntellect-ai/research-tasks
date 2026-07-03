# test_final_state.py

import os
import time
import subprocess
import pytest

def test_binary_exists():
    path = "/home/user/bin/net-aggregator"
    assert os.path.isfile(path), f"Compiled binary not found at {path}"
    assert os.access(path, os.X_OK), f"File at {path} is not executable"

def test_config_correct():
    conf_path = "/home/user/app.conf"
    assert os.path.isfile(conf_path), f"Configuration file {conf_path} not found"
    with open(conf_path, "r") as f:
        content = f.read()
    assert "API_KEY=f47ac10b-58cc-4372-a567-0e02b2c3d479" in content, f"Expected API_KEY with the correct UUID in {conf_path}"

def test_metrics_env():
    env_path = "/home/user/metrics.env"
    assert os.path.isfile(env_path), f"Environment file {env_path} not found"
    with open(env_path, "r") as f:
        content = f.read()
    assert "AGGREGATOR_CONF=/home/user/app.conf" in content, f"Expected AGGREGATOR_CONF to point to /home/user/app.conf in {env_path}"

def test_execution_time_and_success():
    script_path = "/home/user/start_metrics.sh"
    assert os.path.isfile(script_path), f"Wrapper script {script_path} not found"

    # Measure the execution time of the script
    start_time = time.time()
    result = subprocess.run(["bash", script_path], capture_output=True, text=True)
    elapsed_time = time.time() - start_time

    # Check if the script executed successfully
    assert result.returncode == 0, (
        f"start_metrics.sh failed with exit code {result.returncode}.\n"
        f"STDOUT:\n{result.stdout}\n"
        f"STDERR:\n{result.stderr}\n"
        "Ensure the background listener is running and the C program is correctly compiled."
    )

    # Check the performance metric
    threshold = 0.5
    assert elapsed_time <= threshold, (
        f"Execution time {elapsed_time:.3f}s exceeded the threshold of {threshold}s. "
        "The string concatenation in parser.c might still be O(N^2)."
    )