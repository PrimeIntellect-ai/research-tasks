# test_final_state.py

import os
import stat
import subprocess
import time
import pytest
import sys

# Ensure the vendored package is in the path to import parser.py
sys.path.insert(0, "/app/quotalogger-2.1")
try:
    from quotalogger.parser import calculate_quotas
except ImportError:
    calculate_quotas = None

def test_service_dependencies():
    path = "/app/quotalogger-2.1/systemd/quotalogger.service"
    assert os.path.isfile(path), f"Service template {path} is missing."
    with open(path, 'r') as f:
        content = f.read()
    assert "After=mock-db.service" in content, "Service template missing After=mock-db.service."
    assert "Requires=mock-db.service" in content, "Service template missing Requires=mock-db.service."

def test_service_is_active():
    try:
        result = subprocess.run(
            ["systemctl", "--user", "is-active", "quotalogger.service"], 
            capture_output=True, 
            text=True
        )
        assert result.stdout.strip() == "active", f"quotalogger.service is not active. Output: {result.stdout.strip()}"
    except FileNotFoundError:
        pytest.fail("systemctl command not found.")

def test_ci_script_and_results():
    script_path = "/home/user/ci_check.sh"
    assert os.path.isfile(script_path), f"CI script {script_path} is missing."
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"CI script {script_path} is not executable."

    results_path = "/home/user/ci_results.txt"
    if os.path.exists(results_path):
        os.remove(results_path)

    try:
        subprocess.run([script_path], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"CI script failed to run: {e.stderr}")

    assert os.path.isfile(results_path), f"CI results file {results_path} was not created by the script."
    with open(results_path, 'r') as f:
        content = f.read().strip()

    assert content.isdigit(), f"CI results file should contain only a numeric value, got: '{content}'"

def test_parser_performance():
    assert calculate_quotas is not None, "Could not import calculate_quotas from quotalogger.parser"

    test_log_path = "/app/data/test_logs.txt"
    assert os.path.isfile(test_log_path), f"Test logs missing at {test_log_path}"

    start_time = time.time()
    result = calculate_quotas(test_log_path)
    end_time = time.time()
    runtime = end_time - start_time

    assert runtime < 1.0, f"Parser performance metric failed: runtime {runtime:.3f}s >= 1.0s threshold."