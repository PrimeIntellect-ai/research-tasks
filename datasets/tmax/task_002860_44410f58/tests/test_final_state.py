# test_final_state.py
import requests
import pytest
import time
import math

def wait_for_server(url, timeout=5):
    start = time.time()
    while time.time() - start < timeout:
        try:
            r = requests.get(url)
            if r.status_code == 200:
                return True
        except requests.ConnectionError:
            pass
        time.sleep(0.5)
    return False

def test_stats_endpoint():
    url = "http://127.0.0.1:9090/stats"
    assert wait_for_server(url), "Server is not running or /stats endpoint is not accessible."

    response = requests.get(url)
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail("Response is not valid JSON")

    assert isinstance(data, list), "Expected a JSON array"
    assert len(data) >= 20, f"Expected at least 20 elements, got {len(data)}"

    # Check index 6
    item_6 = data[6]
    assert "anomaly_score" in item_6, "Missing anomaly_score in JSON"
    assert "rolling_avg" in item_6, "Missing rolling_avg in JSON"

    assert math.isclose(item_6["anomaly_score"], 5.0, abs_tol=0.1), f"Expected anomaly_score ~5.0 at second 6, got {item_6['anomaly_score']}"
    assert math.isclose(item_6["rolling_avg"], 3.2, abs_tol=0.1), f"Expected rolling_avg ~3.2 at second 6, got {item_6['rolling_avg']}"

def test_report_endpoint():
    url = "http://127.0.0.1:9090/report"
    assert wait_for_server(url), "Server is not running or /report endpoint is not accessible."

    response = requests.get(url)
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    text = response.text
    assert "Maximum Rolling Anomaly Score" in text, "Report missing 'Maximum Rolling Anomaly Score'"
    assert "5" in text, "Report missing max score value"
    assert "9" in text, "Report missing second offset"