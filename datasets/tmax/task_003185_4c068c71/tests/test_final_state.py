# test_final_state.py
import os
import requests

def test_health_endpoint():
    """Verify that Nginx is proxying correctly to the Python backend."""
    try:
        response = requests.get("http://127.0.0.1:8080/health", timeout=5)
    except requests.exceptions.RequestException as e:
        assert False, f"Failed to connect to Nginx on port 8080 or upstream is down: {e}"

    assert response.status_code == 200, f"Expected status code 200 from /health, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        assert False, f"Expected JSON response from /health, got: {response.text}"

    assert data.get("status") == "ok", f"Expected status 'ok', got {data.get('status')}"

def test_metrics_endpoint():
    """Verify that the /metrics endpoint returns the correct aggregated costs."""
    try:
        response = requests.get("http://127.0.0.1:8080/metrics", timeout=5)
    except requests.exceptions.RequestException as e:
        assert False, f"Failed to connect to Nginx on port 8080 or upstream is down: {e}"

    assert response.status_code == 200, f"Expected status code 200 from /metrics, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        assert False, f"Expected JSON response from /metrics, got: {response.text}"

    # Expected aggregated costs derived from the billing.log
    expected_costs = {
        "EC2": 15.50,
        "S3": 4.00,
        "RDS": 15.00
    }

    for service, expected_val in expected_costs.items():
        assert service in data, f"Missing service '{service}' in JSON response. Got: {data}"
        actual_val = float(data[service])
        assert abs(actual_val - expected_val) < 0.01, f"Expected {expected_val} for {service}, got {actual_val}"

def test_api_py_uses_subprocess():
    """Verify that the implementation uses subprocess as per the instructions."""
    path = "/home/user/app/api.py"
    assert os.path.exists(path), f"{path} is missing"
    with open(path, "r") as f:
        content = f.read()

    assert "subprocess" in content, "api.py does not appear to use subprocess to calculate the costs."