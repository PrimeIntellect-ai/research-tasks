# test_final_state.py
import requests
import pytest
import math
import os

def test_result_json_via_http():
    url = "http://127.0.0.1:8080/result.json"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the HTTP server at {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response from {url} is not valid JSON. Response text: {response.text}")

    assert "total_extrusion" in data, "Missing 'total_extrusion' in JSON response"
    assert "final_status" in data, "Missing 'final_status' in JSON response"
    assert "flash_frames" in data, "Missing 'flash_frames' in JSON response"

    assert math.isclose(data["total_extrusion"], 4.0, rel_tol=1e-5), f"Expected total_extrusion to be 4.0, got {data['total_extrusion']}"
    assert data["final_status"] == "Finished", f"Expected final_status to be 'Finished', got {data['final_status']}"
    assert data["flash_frames"] == 3, f"Expected flash_frames to be 3, got {data['flash_frames']}"

def test_malicious_file_not_extracted():
    # The tar contains ../malicious_file.txt. If extracted naively in /home/user/extracted,
    # it would end up in /home/user/malicious_file.txt
    malicious_path = "/home/user/malicious_file.txt"
    assert not os.path.exists(malicious_path), f"Malicious file was extracted to {malicious_path}! Archive integrity verification failed."