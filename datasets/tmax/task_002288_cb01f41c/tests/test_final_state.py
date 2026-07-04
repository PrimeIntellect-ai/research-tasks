# test_final_state.py

import os
import time
import requests
import pytest

BASE_URL = "http://127.0.0.1:8080"

def wait_for_service():
    """Wait for the HTTP service to become available."""
    for _ in range(30):
        try:
            requests.get(f"{BASE_URL}/api/deadlocks", timeout=1)
            return True
        except requests.exceptions.RequestException:
            time.sleep(1)
    return False

@pytest.fixture(scope="module", autouse=True)
def ensure_service_running():
    assert wait_for_service(), "The HTTP service on 127.0.0.1:8080 did not start or is unreachable."

def test_transactions_csv_exists():
    csv_path = "/home/user/transactions.csv"
    assert os.path.exists(csv_path), f"Expected CSV file {csv_path} does not exist."
    assert os.path.isfile(csv_path), f"{csv_path} is not a file."

def test_api_deadlocks():
    url = f"{BASE_URL}/api/deadlocks"
    response = requests.get(url, timeout=5)
    assert response.status_code == 200, f"Expected status 200, got {response.status_code} for {url}"

    data = response.json()
    expected = [101, 102, 103, 104, 105, 106]
    assert data == expected, f"Expected deadlocks {expected}, got {data}"

def test_api_centrality():
    url = f"{BASE_URL}/api/centrality?limit=3"
    response = requests.get(url, timeout=5)
    assert response.status_code == 200, f"Expected status 200, got {response.status_code} for {url}"

    data = response.json()
    expected = [
        {"account": 101, "out_degree": 2},
        {"account": 102, "out_degree": 1},
        {"account": 103, "out_degree": 1}
    ]
    assert data == expected, f"Expected centrality {expected}, got {data}"

def test_api_path():
    url = f"{BASE_URL}/api/path?src=102&dst=106"
    response = requests.get(url, timeout=5)
    assert response.status_code == 200, f"Expected status 200, got {response.status_code} for {url}"

    data = response.json()
    expected = [102, 103, 101, 104, 105, 106]
    assert data == expected, f"Expected path {expected}, got {data}"

def test_server_log_exists():
    log_path = "/home/user/server.log"
    assert os.path.exists(log_path), f"Expected log file {log_path} does not exist."
    assert os.path.isfile(log_path), f"{log_path} is not a file."