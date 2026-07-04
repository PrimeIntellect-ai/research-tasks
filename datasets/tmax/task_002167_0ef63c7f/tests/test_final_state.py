# test_final_state.py
import pytest
import requests
import time

BASE_URL = "http://127.0.0.1:8080"

def wait_for_service(url, timeout=10):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(url)
            if response.status_code in [200, 404, 405]:
                return True
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(0.5)
    return False

@pytest.fixture(scope="module", autouse=True)
def check_service_up():
    assert wait_for_service(f"{BASE_URL}/anomalies"), f"Service at {BASE_URL} did not start or is not reachable."

def test_anomalies_endpoint():
    url = f"{BASE_URL}/anomalies"
    response = requests.get(url)
    assert response.status_code == 200, f"Expected 200 OK from {url}, got {response.status_code}"

    data = response.json()
    assert "anomalies" in data, "Response JSON missing 'anomalies' key"

    anomalies = data["anomalies"]
    assert isinstance(anomalies, list), "'anomalies' should be a list"
    assert anomalies == [10, 20], f"Expected anomalies to be [10, 20], got {anomalies}"

def test_correlation_endpoint_normal():
    url = f"{BASE_URL}/correlation?f1=0&f2=1"
    response = requests.get(url)
    assert response.status_code == 200, f"Expected 200 OK from {url}, got {response.status_code}"

    data = response.json()
    assert "correlation" in data, "Response JSON missing 'correlation' key"

    corr = data["correlation"]
    assert isinstance(corr, (int, float)), "'correlation' should be a number"
    assert corr >= 0.85, f"Expected correlation between frame 0 and 1 to be >= 0.85, got {corr}"

def test_correlation_endpoint_anomaly():
    url = f"{BASE_URL}/correlation?f1=9&f2=10"
    response = requests.get(url)
    assert response.status_code == 200, f"Expected 200 OK from {url}, got {response.status_code}"

    data = response.json()
    assert "correlation" in data, "Response JSON missing 'correlation' key"

    corr = data["correlation"]
    assert isinstance(corr, (int, float)), "'correlation' should be a number"
    assert corr < 0.85, f"Expected correlation between frame 9 and 10 to be < 0.85, got {corr}"