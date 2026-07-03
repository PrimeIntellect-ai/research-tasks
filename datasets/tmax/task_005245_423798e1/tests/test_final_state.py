# test_final_state.py

import pytest
import requests

BASE_URL = "http://127.0.0.1:9090/localize"

def test_localize_es_es():
    payload = {
        "locale": "es-ES",
        "start_time": 1000,
        "end_time": 1030,
        "interval": 10,
        "events": {"1000": "Welcome", "1030": "Error"}
    }
    try:
        response = requests.post(BASE_URL, json=payload, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {BASE_URL}: {e}")

    assert response.status_code == 200, f"Expected status 200, got {response.status_code}. Response: {response.text}"

    expected_lines = [
        "[1000] Bienvenido",
        "[1010] Inactivo",
        "[1020] Inactivo",
        "[1030] Error"
    ]
    actual_lines = response.text.strip().split("\n")
    assert actual_lines == expected_lines, f"Expected {expected_lines}, got {actual_lines}"

def test_localize_fr_fr():
    payload = {
        "locale": "fr-FR",
        "start_time": 2000,
        "end_time": 2010,
        "interval": 10,
        "events": {"2010": "Warning"}
    }
    try:
        response = requests.post(BASE_URL, json=payload, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {BASE_URL}: {e}")

    assert response.status_code == 200, f"Expected status 200, got {response.status_code}. Response: {response.text}"

    expected_lines = [
        "[2000] Inactif",
        "[2010] Avertissement"
    ]
    actual_lines = response.text.strip().split("\n")
    assert actual_lines == expected_lines, f"Expected {expected_lines}, got {actual_lines}"

def test_localize_invalid_locale():
    payload = {
        "locale": "de-DE",
        "start_time": 3000,
        "end_time": 3010,
        "interval": 10,
        "events": {}
    }
    try:
        response = requests.post(BASE_URL, json=payload, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {BASE_URL}: {e}")

    assert response.status_code == 400, f"Expected status 400 for invalid locale, got {response.status_code}. Response: {response.text}"