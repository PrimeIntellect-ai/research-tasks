# test_final_state.py

import time
import socket
import pytest
import requests

BASE_URL = "http://127.0.0.1:8080"

@pytest.fixture(scope="session", autouse=True)
def wait_for_server():
    """Wait for the C HTTP service to bind to port 8080."""
    max_retries = 10
    for _ in range(max_retries):
        try:
            with socket.create_connection(("127.0.0.1", 8080), timeout=1):
                return
        except OSError:
            time.sleep(0.5)
    pytest.fail("Service is not listening on 127.0.0.1:8080. Is the C application running?")

def test_service_workflow():
    """
    Test the complete workflow described in the verifier logic:
    - POST /config with new logs
    - GET /stats to check averages
    - POST duplicate TXN to test deduplication
    - POST more logs to test rolling window (size 5)
    """
    # 2. POST T01
    res = requests.post(f"{BASE_URL}/config", data="[TXN:T01] SET a=1 SIZE=10")
    assert res.status_code == 200, f"Expected 200 OK for POST /config, got {res.status_code}"

    # 3. POST T02
    res = requests.post(f"{BASE_URL}/config", data="[TXN:T02] SET b=2 SIZE=20")
    assert res.status_code == 200, f"Expected 200 OK for POST /config, got {res.status_code}"

    # 4. GET /stats
    res = requests.get(f"{BASE_URL}/stats")
    assert res.status_code == 200, f"Expected 200 OK for GET /stats, got {res.status_code}"
    assert res.text == "Average: 15.00\n", f"Expected 'Average: 15.00\\n', got {repr(res.text)}"

    # 5. POST T01 (Duplicate)
    res = requests.post(f"{BASE_URL}/config", data="[TXN:T01] SET a=1 SIZE=500")
    assert res.status_code == 200, f"Expected 200 OK for POST /config (duplicate), got {res.status_code}"

    # 6. GET /stats (Verify deduplication)
    res = requests.get(f"{BASE_URL}/stats")
    assert res.status_code == 200
    assert res.text == "Average: 15.00\n", f"Deduplication failed. Expected 'Average: 15.00\\n', got {repr(res.text)}"

    # 7. POST 4 more unique requests
    requests.post(f"{BASE_URL}/config", data="[TXN:T03] SET c=3 SIZE=30")
    requests.post(f"{BASE_URL}/config", data="[TXN:T04] SET d=4 SIZE=40")
    requests.post(f"{BASE_URL}/config", data="[TXN:T05] SET e=5 SIZE=50")
    requests.post(f"{BASE_URL}/config", data="[TXN:T06] SET f=6 SIZE=60")

    # 8 & 9. GET /stats (Verify rolling window of size 5)
    # The elements should be T02(20), T03(30), T04(40), T05(50), T06(60) -> Average: 40.00
    res = requests.get(f"{BASE_URL}/stats")
    assert res.status_code == 200
    assert res.text == "Average: 40.00\n", f"Rolling window failed. Expected 'Average: 40.00\\n', got {repr(res.text)}"