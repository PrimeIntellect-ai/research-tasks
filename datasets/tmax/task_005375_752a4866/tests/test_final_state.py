# test_final_state.py

import os
import subprocess
import time
import requests
import pytest

def test_services_running():
    # Check if aggregator is running
    try:
        res = requests.get("http://localhost:5000/results", timeout=2)
        assert res.status_code in [200, 404, 405], "Aggregator service did not respond properly."
    except requests.exceptions.RequestException:
        pytest.fail("Aggregator service is not running on port 5000.")

    # Check if Go integrator is running
    try:
        res = requests.post("http://localhost:8080/solve", timeout=2)
        # Should be 401 Unauthorized because of missing header
        assert res.status_code == 401, f"Expected 401 Unauthorized without header, got {res.status_code}"
    except requests.exceptions.RequestException:
        pytest.fail("Go Integrator service is not running on port 8080.")

def test_go_integrator_auth():
    headers = {"Authorization": "Bearer ds-model-fit-token"}
    try:
        res = requests.post("http://localhost:8080/solve", headers=headers, timeout=5)
        assert res.status_code in [200, 202], f"Expected success with auth header, got {res.status_code}"
    except requests.exceptions.RequestException:
        pytest.fail("Failed to connect to Go Integrator service with auth header.")

def test_results_log_exists():
    results_path = "/home/user/results.log"
    assert os.path.exists(results_path), f"{results_path} does not exist."
    assert os.path.getsize(results_path) > 0, f"{results_path} is empty."

def test_solver_fixed():
    solver_path = "/home/user/app/integrator/solver.go"
    assert os.path.exists(solver_path), f"{solver_path} is missing."
    with open(solver_path, "r") as f:
        content = f.read()
        assert "1e-6" in content, "The minimum step size 1e-6 is not enforced in solver.go."
        assert "math.Pow" in content or "Pow(" in content or "1e-6" in content, "Step size adaptation logic does not seem to be fixed."

def test_main_parallel():
    main_path = "/home/user/app/integrator/main.go"
    assert os.path.exists(main_path), f"{main_path} is missing."
    with open(main_path, "r") as f:
        content = f.read()
        assert "sync.WaitGroup" in content or "WaitGroup" in content, "WaitGroup is missing in main.go."
        assert "go " in content, "Goroutines are not used in main.go."