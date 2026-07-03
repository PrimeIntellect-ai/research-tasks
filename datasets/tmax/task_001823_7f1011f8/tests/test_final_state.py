# test_final_state.py

import os
import time
import subprocess
import requests
import statistics
import pytest

APP_DIR = "/home/user/app"

@pytest.fixture(scope="module")
def running_services():
    """Start the services and ensure they are torn down after tests."""
    proc = subprocess.Popen(
        ["bash", "start.sh"],
        cwd=APP_DIR,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    # Give services time to start up
    time.sleep(5)

    yield

    proc.terminate()
    proc.wait()

def test_aggregator_variance_and_parsing(running_services):
    """
    Test that the aggregator can parse edge-case JSON payloads and 
    computes variance with numerical stability (avoiding catastrophic cancellation).
    """
    N = 10000
    base_value = 1e9

    # Calculate exact sample variance using Python's high-precision statistics module
    values = [base_value + i for i in range(N)]
    reference_variance = statistics.variance(values)

    session = requests.Session()
    headers = {"Content-Type": "application/json"}

    for i in range(N):
        val = values[i]

        # Inject the edge-case formats mentioned in the prompt
        if i % 3 == 0:
            # Trailing comma
            payload = f'{{"value": {val},}}'
        elif i % 3 == 1:
            # String-encoded scientific notation
            payload = f'{{"value": "{val}e0"}}'
        else:
            # Standard JSON float
            payload = f'{{"value": {val}}}'

        try:
            res = session.post("http://localhost:5000/record", data=payload, headers=headers, timeout=2)
            assert res.status_code == 200, f"Aggregator rejected payload: {payload}. Status: {res.status_code}"
        except requests.exceptions.ConnectionError:
            pytest.fail("Failed to connect to Aggregator on port 5000. Is it running and connected to Redis?")

    # Fetch the computed metrics
    try:
        res = session.get("http://localhost:5000/metrics", timeout=2)
        assert res.status_code == 200, "Failed to get metrics from Aggregator"
    except requests.exceptions.ConnectionError:
        pytest.fail("Failed to connect to Aggregator to fetch metrics.")

    data = res.json()
    assert "variance" in data, "Response JSON is missing the 'variance' key."

    agent_variance = float(data["variance"])

    # Calculate Mean Squared Error of the single variance metric
    mse = (agent_variance - reference_variance) ** 2
    threshold = 1e-10

    assert mse <= threshold, (
        f"Variance calculation is not numerically stable.\n"
        f"MSE {mse} exceeds threshold {threshold}.\n"
        f"Agent variance: {agent_variance}\n"
        f"Reference variance: {reference_variance}"
    )