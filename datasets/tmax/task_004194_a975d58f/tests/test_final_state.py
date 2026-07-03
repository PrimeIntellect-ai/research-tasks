# test_final_state.py

import json
import base64
import requests
import pytest

BASE_URL = "http://127.0.0.1:9090"

def test_resolve_endpoint():
    """Verify that the POST /resolve endpoint correctly patches the manifest."""
    graph_data = b"dummy_graph"
    manifest_data = b'{\n  "name": "mobile-app"\n}'

    payload = {
        "graph_b64": base64.b64encode(graph_data).decode('utf-8'),
        "manifest_b64": base64.b64encode(manifest_data).decode('utf-8')
    }

    try:
        response = requests.post(f"{BASE_URL}/resolve", json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to POST /resolve endpoint: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    try:
        resp_json = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert "patched_manifest" in resp_json, "Response JSON missing 'patched_manifest' key."

    expected_patched = '{\n  "dependencies_resolved": true,\n  "name": "mobile-app"\n}'
    assert resp_json["patched_manifest"] == expected_patched, (
        f"Patched manifest does not match expected output.\n"
        f"Expected:\n{expected_patched}\nGot:\n{resp_json['patched_manifest']}"
    )

def test_benchmark_endpoint():
    """Verify that the GET /benchmark endpoint returns a valid average execution time."""
    try:
        response = requests.get(f"{BASE_URL}/benchmark", timeout=30)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to GET /benchmark endpoint: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    try:
        resp_json = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert "avg_time_ms" in resp_json, "Response JSON missing 'avg_time_ms' key."

    avg_time = resp_json["avg_time_ms"]
    assert isinstance(avg_time, (int, float)), f"'avg_time_ms' should be a number, got {type(avg_time)}."
    assert avg_time >= 0, f"'avg_time_ms' should be non-negative, got {avg_time}."