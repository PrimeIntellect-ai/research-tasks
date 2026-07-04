# test_final_state.py

import pytest
import requests

def test_server_zone_alpha():
    url = "http://127.0.0.1:8080/rolling?zone=zone_alpha"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    assert "text/csv" in response.headers.get("Content-Type", ""), "Expected Content-Type to include text/csv"

    expected_csv = (
        "timestamp,value,rolling_avg\n"
        "100,10.00,10.00\n"
        "101,15.00,12.50\n"
        "102,14.00,13.00\n"
        "103,20.00,16.33\n"
        "104,22.00,18.67"
    )

    actual_csv = response.text.strip().replace("\r\n", "\n")
    assert actual_csv == expected_csv, f"Response for zone_alpha did not match expected CSV.\nExpected:\n{expected_csv}\nActual:\n{actual_csv}"

def test_server_zone_beta():
    url = "http://127.0.0.1:8080/rolling?zone=zone_beta"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    expected_csv = (
        "timestamp,value,rolling_avg\n"
        "100,5.00,5.00\n"
        "101,6.00,5.50\n"
        "102,8.00,6.33\n"
        "103,7.00,7.00\n"
        "104,10.00,8.33"
    )

    actual_csv = response.text.strip().replace("\r\n", "\n")
    assert actual_csv == expected_csv, f"Response for zone_beta did not match expected CSV.\nExpected:\n{expected_csv}\nActual:\n{actual_csv}"

def test_server_zone_gamma():
    url = "http://127.0.0.1:8080/rolling?zone=zone_gamma"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    expected_csv = (
        "timestamp,value,rolling_avg\n"
        "100,100.00,100.00\n"
        "101,90.00,95.00\n"
        "102,80.00,90.00\n"
        "103,85.00,85.00\n"
        "104,88.00,84.33"
    )

    actual_csv = response.text.strip().replace("\r\n", "\n")
    assert actual_csv == expected_csv, f"Response for zone_gamma did not match expected CSV.\nExpected:\n{expected_csv}\nActual:\n{actual_csv}"