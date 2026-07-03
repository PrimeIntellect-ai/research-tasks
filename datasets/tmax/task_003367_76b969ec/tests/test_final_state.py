# test_final_state.py

import requests
import pytest

def test_timeserver_port_and_bug_ticket_fix():
    url = "http://127.0.0.1:9090/convert"
    params = {"datetime": "2023-10-29T01:30:00-CET"}

    try:
        response = requests.get(url, params=params, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail("The timeserver is not running or not listening on 127.0.0.1:9090.")
    except requests.exceptions.Timeout:
        pytest.fail("The timeserver timed out when requesting the CET datetime.")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"
    assert response.text.strip() == "1698543000", f"Expected body '1698543000', got {response.text!r}"

def test_timeserver_utc_conversion():
    url = "http://127.0.0.1:9090/convert"
    params = {"datetime": "2024-01-01T12:00:00-UTC"}

    try:
        response = requests.get(url, params=params, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail("The timeserver is not running or not listening on 127.0.0.1:9090.")
    except requests.exceptions.Timeout:
        pytest.fail("The timeserver timed out when requesting the UTC datetime.")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"
    assert response.text.strip() == "1704110400", f"Expected body '1704110400', got {response.text!r}"