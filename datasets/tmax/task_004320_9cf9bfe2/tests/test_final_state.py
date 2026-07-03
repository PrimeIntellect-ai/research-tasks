# test_final_state.py

import pytest
import requests
import math

BASE_URL = "http://127.0.0.1:8080"
API_KEY = "sec_prod_99x8a7f6b5c4d3e2f1"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def test_service_is_listening():
    """Verify the service is running and accepting connections."""
    try:
        # We don't assert the status code here, just that the port is bound and listening
        requests.get(BASE_URL, timeout=2)
    except requests.exceptions.ConnectionError:
        pytest.fail(f"Service is not listening on {BASE_URL}. Did you start it in the background?")
    except requests.exceptions.Timeout:
        pytest.fail(f"Service at {BASE_URL} timed out.")

def test_unauthorized_request_rejected():
    """Verify that the service rejects requests without the correct API key."""
    try:
        res = requests.post(f"{BASE_URL}/tick", json={"symbol": "TEST", "price": 100.0, "qty": 10}, timeout=2)
        assert res.status_code in (401, 403), f"Expected 401 or 403 for missing auth, got {res.status_code}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to service: {e}")

def test_qty_zero_bad_request():
    """Verify that a tick with qty=0 is rejected with a 400 Bad Request."""
    payload = {"symbol": "ZERO", "price": 50000.0, "qty": 0}
    try:
        res = requests.post(f"{BASE_URL}/tick", headers=HEADERS, json=payload, timeout=2)
        assert res.status_code == 400, f"Expected 400 Bad Request for qty=0, got {res.status_code}. Body: {res.text}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to service: {e}")

def test_vwap_precision_f64():
    """Verify that the VWAP calculation uses f64 precision."""
    symbol = "PRECISION_TEST"

    tick1 = {"symbol": symbol, "price": 60000.12345678901, "qty": 10}
    tick2 = {"symbol": symbol, "price": 60000.98765432109, "qty": 5}

    try:
        res1 = requests.post(f"{BASE_URL}/tick", headers=HEADERS, json=tick1, timeout=2)
        assert res1.status_code == 200, f"Failed to post tick 1: {res1.status_code} - {res1.text}"

        res2 = requests.post(f"{BASE_URL}/tick", headers=HEADERS, json=tick2, timeout=2)
        assert res2.status_code == 200, f"Failed to post tick 2: {res2.status_code} - {res2.text}"

        res_vwap = requests.get(f"{BASE_URL}/vwap?symbol={symbol}", headers=HEADERS, timeout=2)
        assert res_vwap.status_code == 200, f"Failed to get VWAP: {res_vwap.status_code} - {res_vwap.text}"

        data = res_vwap.json()
        assert "vwap" in data, f"Response JSON missing 'vwap' field: {data}"

        expected_vwap = (tick1["price"] * tick1["qty"] + tick2["price"] * tick2["qty"]) / (tick1["qty"] + tick2["qty"])
        actual_vwap = data["vwap"]

        # If f32 is used, precision loss will be significant (error > 1e-4)
        # With f64, it should be highly accurate
        assert math.isclose(actual_vwap, expected_vwap, rel_tol=1e-12), \
            f"VWAP precision issue. Expected {expected_vwap}, got {actual_vwap}. Are you sure you upgraded to f64?"

    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to service: {e}")