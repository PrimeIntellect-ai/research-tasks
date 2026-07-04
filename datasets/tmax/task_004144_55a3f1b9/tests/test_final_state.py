# test_final_state.py

import pytest
import requests
import math

URL = "http://127.0.0.1:8080/process"

def check_response(payload, expected_triangles, expected_score):
    try:
        response = requests.post(URL, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server or send request: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Response text: {response.text}")

    assert "triangles" in data, f"Missing 'triangles' key in JSON response: {data}"
    assert "oracle_score" in data, f"Missing 'oracle_score' key in JSON response: {data}"

    assert data["triangles"] == expected_triangles, f"Expected {expected_triangles} triangles, got {data['triangles']}"
    assert math.isclose(data["oracle_score"], expected_score, rel_tol=1e-3, abs_tol=1e-3), \
        f"Expected oracle_score ~{expected_score}, got {data['oracle_score']}"

def test_process_graph_1():
    payload = {"nodes": 4, "edges": [[0,1], [1,2], [2,3], [3,0], [0,2]]}
    check_response(payload, 2, 13.9)

def test_process_graph_2():
    payload = {"nodes": 3, "edges": [[0,1], [1,2]]}
    check_response(payload, 0, 3.0)

def test_process_graph_3_k5():
    # K5 graph
    edges = []
    for i in range(5):
        for j in range(i + 1, 5):
            edges.append([i, j])
    payload = {"nodes": 5, "edges": edges}
    # 10 edges, 10 triangles
    # score = 10 * 1.5 + 10 * 3.2 = 15.0 + 32.0 = 47.0
    check_response(payload, 10, 47.0)

def test_process_graph_4_disconnected():
    payload = {"nodes": 6, "edges": [[0,1], [1,2], [2,0], [3,4], [4,5], [5,3]]}
    # 6 edges, 2 triangles
    # score = 6 * 1.5 + 2 * 3.2 = 9.0 + 6.4 = 15.4
    check_response(payload, 2, 15.4)