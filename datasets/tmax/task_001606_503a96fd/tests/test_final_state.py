# test_final_state.py

import socket
import json
import pytest

def test_service_response():
    host = '127.0.0.1'
    port = 8585

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5.0)
        s.connect((host, port))
    except Exception as e:
        pytest.fail(f"Could not connect to {host}:{port}: {e}")

    try:
        s.sendall(b"GET_REPORT\n")
        response = b""
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            response += chunk
            if b"}" in response:
                break
    except Exception as e:
        pytest.fail(f"Error communicating with service: {e}")
    finally:
        s.close()

    assert response, "Received empty response from service"

    try:
        data = json.loads(response.decode('utf-8').strip())
    except json.JSONDecodeError as e:
        pytest.fail(f"Response is not valid JSON: {e}\nResponse was: {response}")

    expected_keys = {
        "candidate_energy",
        "candidate_zcr",
        "baseline_energy_ci",
        "baseline_zcr_ci",
        "is_anomaly"
    }

    assert set(data.keys()) == expected_keys, f"JSON keys do not match expected. Got: {list(data.keys())}"

    assert isinstance(data["candidate_energy"], (int, float)), "candidate_energy must be a number"
    assert isinstance(data["candidate_zcr"], (int, float)), "candidate_zcr must be a number"
    assert isinstance(data["baseline_energy_ci"], list) and len(data["baseline_energy_ci"]) == 2, "baseline_energy_ci must be a list of 2 numbers"
    assert isinstance(data["baseline_zcr_ci"], list) and len(data["baseline_zcr_ci"]) == 2, "baseline_zcr_ci must be a list of 2 numbers"
    assert isinstance(data["is_anomaly"], bool), "is_anomaly must be a boolean"