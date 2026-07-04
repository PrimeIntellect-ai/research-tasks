# test_final_state.py
import os
import subprocess
import time
import socket
import pytest
import requests
import numpy as np

@pytest.fixture(scope="session", autouse=True)
def start_server():
    script_path = "/home/user/run_server.sh"
    assert os.path.exists(script_path), f"{script_path} does not exist"

    # Ensure the script is executable
    os.chmod(script_path, 0o755)

    # Start the server in the background
    process = subprocess.Popen(
        [script_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )

    # Wait for port 8000 to open
    port_open = False
    for _ in range(30):
        try:
            with socket.create_connection(("127.0.0.1", 8000), timeout=1):
                port_open = True
                break
        except OSError:
            time.sleep(1)

    if not port_open:
        os.killpg(os.getpgid(process.pid), 15)
        pytest.fail("Server did not start on port 8000 within 30 seconds.")

    yield

    # Teardown: kill the process group
    try:
        os.killpg(os.getpgid(process.pid), 15)
    except Exception:
        pass

def test_unauthorized_access():
    response = requests.get("http://127.0.0.1:8000/integrate?t=5.0")
    assert response.status_code == 401, f"Expected 401 Unauthorized without token, got {response.status_code}"

def test_integrate_endpoint():
    headers = {"Authorization": "Bearer BIO-77X9"}
    response = requests.get("http://127.0.0.1:8000/integrate?t=5.0", headers=headers)
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except Exception:
        pytest.fail(f"Could not parse JSON from response: {response.text}")

    assert "integral" in data, "Response JSON missing 'integral' key"

    integral_val = data["integral"]
    expected_val = 1.5 * (5.0**3 / 3.0)  # 62.5
    assert abs(integral_val - expected_val) < 1e-4, f"Expected integral ~{expected_val}, got {integral_val}"

def test_bootstrap_endpoint():
    headers = {"Authorization": "Bearer BIO-77X9"}
    response = requests.get("http://127.0.0.1:8000/bootstrap", headers=headers)
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except Exception:
        pytest.fail(f"Could not parse JSON from response: {response.text}")

    assert "ci_lower" in data, "Response JSON missing 'ci_lower' key"
    assert "ci_upper" in data, "Response JSON missing 'ci_upper' key"

    # Compute the expected bootstrap confidence interval
    scores = np.array([1.2, 1.5, 1.3, 1.7, 1.1, 1.9, 1.4, 1.6, 1.8, 1.5])
    np.random.seed(42)
    means = [np.mean(np.random.choice(scores, size=len(scores), replace=True)) for _ in range(1000)]
    expected_lower = np.percentile(means, 2.5)
    expected_upper = np.percentile(means, 97.5)

    assert abs(data["ci_lower"] - expected_lower) < 0.01, f"Expected ci_lower ~{expected_lower}, got {data['ci_lower']}"
    assert abs(data["ci_upper"] - expected_upper) < 0.01, f"Expected ci_upper ~{expected_upper}, got {data['ci_upper']}"