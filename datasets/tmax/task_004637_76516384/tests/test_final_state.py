# test_final_state.py

import os
import socket
import time
import requests
import pytest

def test_simulation_pipeline():
    # Payload as described in the prompt
    payload = {
        "data": "0.0,10.0,0.1\n0.1,9.8,0.2\n0.2,9.5,0.8\n0.3,9.1,0.1"
    }

    # 1. Send HTTP POST to API Gateway
    try:
        response = requests.post("http://127.0.0.1:8080/simulate", json=payload, timeout=5)
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to API Gateway at 127.0.0.1:8080: {e}")

    # Give the simulation a moment to run and send results to the aggregator
    time.sleep(2)

    # 2. Connect to TCP Aggregator and get results
    try:
        with socket.create_connection(("127.0.0.1", 9090), timeout=5) as sock:
            sock.sendall(b"GET_RESULTS\n")
            data = sock.recv(1024).decode('utf-8').strip()
    except Exception as e:
        pytest.fail(f"Failed to connect to Aggregator at 127.0.0.1:9090 or retrieve results: {e}")

    assert data, "Received empty response from Aggregator"

    try:
        result_val = float(data)
    except ValueError:
        pytest.fail(f"Expected a floating point number from Aggregator, got: {data}")

    # Check that the result is numerically stable (not NaN/Inf) and in the expected range
    import math
    assert not math.isnan(result_val), "Simulation diverged: received NaN"
    assert not math.isinf(result_val), "Simulation diverged: received Infinity"

    # The expected integrated value is approximately 8.5
    assert 5.0 < result_val < 15.0, f"Simulation output {result_val} is outside the expected stable range."

def test_script_modifications():
    # Check reshape_data.sh
    reshape_script = "/home/user/app/scripts/reshape_data.sh"
    assert os.path.isfile(reshape_script), f"Missing {reshape_script}"
    with open(reshape_script, "r") as f:
        content = f.read()
        assert "0.5" in content, "reshape_data.sh does not seem to filter error > 0.5"

    # Check run_mpi_sim.sh
    run_script = "/home/user/app/scripts/run_mpi_sim.sh"
    assert os.path.isfile(run_script), f"Missing {run_script}"
    with open(run_script, "r") as f:
        content = f.read()
        assert "mpirun" in content and "-n 4" in content, "run_mpi_sim.sh does not invoke mpirun with 4 processes"
        assert "venv" in content, "run_mpi_sim.sh does not load the virtual environment"

    # Check simulator.py
    simulator_script = "/home/user/app/simulator.py"
    assert os.path.isfile(simulator_script), f"Missing {simulator_script}"
    with open(simulator_script, "r") as f:
        content = f.read()
        assert "0.01" in content, "simulator.py does not seem to use dt = 0.01"