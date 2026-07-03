# test_final_state.py

import os
import time
import requests
import pytest

SERVICE_URL = "http://127.0.0.1:9090"
AUTH_TOKEN = "Baye$ian2023"
HEADERS = {"Authorization": f"Bearer {AUTH_TOKEN}"}

def wait_for_service(url, timeout=5):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            # Just check if the port is open and responding
            requests.get(f"{url}/aggregate", headers=HEADERS, timeout=1)
            return True
        except requests.exceptions.RequestException:
            time.sleep(0.5)
    return False

def test_service_log_exists():
    """Verify that the service log file was created."""
    log_path = "/home/user/service.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist. Did you redirect stdout/stderr?"

def test_service_running_and_authenticated():
    """Verify the service is running at the correct host/port and accepts the auth token."""
    assert wait_for_service(SERVICE_URL), f"Service is not reachable at {SERVICE_URL} within the timeout."

    # Test unauthorized access
    resp = requests.get(f"{SERVICE_URL}/aggregate")
    assert resp.status_code in (401, 403), f"Expected 401/403 for unauthorized request, got {resp.status_code}"

def test_record_and_aggregate():
    """Verify the /record and /aggregate endpoints work as expected."""
    assert wait_for_service(SERVICE_URL), f"Service is not reachable at {SERVICE_URL}"

    payload = {
        "experiment_id": "test_exp_001",
        "prior_mu": 0.0,
        "prior_sigma": 1.0,
        "likelihood_mu": 1.0,
        "likelihood_sigma": 1.0
    }

    # Test POST /record
    post_resp = requests.post(f"{SERVICE_URL}/record", json=payload, headers=HEADERS)
    assert post_resp.status_code == 200, f"POST /record failed with status {post_resp.status_code}. Response: {post_resp.text}"

    data = post_resp.json()
    assert "posterior_mu" in data, "Response missing 'posterior_mu'"
    assert "posterior_sigma" in data, "Response missing 'posterior_sigma'"

    # Test GET /aggregate
    get_resp = requests.get(f"{SERVICE_URL}/aggregate", headers=HEADERS)
    assert get_resp.status_code == 200, f"GET /aggregate failed with status {get_resp.status_code}. Response: {get_resp.text}"

    agg_data = get_resp.json()
    assert isinstance(agg_data, list), f"Expected /aggregate to return a JSON array, got {type(agg_data)}"

    # Check if our experiment is in the aggregated data
    found = any(exp.get("experiment_id") == "test_exp_001" for exp in agg_data)
    assert found, "The recorded experiment 'test_exp_001' was not found in the /aggregate response."