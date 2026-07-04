# test_final_state.py

import math
import requests
import pytest

BASE_URL = "http://127.0.0.1:8080"
HEADERS = {"Authorization": "Bearer sim-token-2024"}

def get_pdb_payload():
    return """ATOM      1  N   ALA A   1      11.104   6.134  -6.504  1.00  0.00           N
ATOM      2  CA  ALA A   1      11.639   6.071  -5.147  1.00  0.00           C
ATOM      3  C   ALA A   1      10.385   6.095  -4.225  1.00  0.00           C
ATOM      4  CB  ALA A   1      12.441   7.309  -4.887  1.00  0.00           C"""

def calculate_expected_energy():
    atoms = [
        (1, "N", 11.104, 6.134, -6.504),
        (2, "CA", 11.639, 6.071, -5.147),
        (3, "C", 10.385, 6.095, -4.225),
        (4, "CB", 12.441, 7.309, -4.887),
    ]

    weights = {"CA": 1.25, "C": 0.85, "N": 1.10}

    total_energy = 0.0
    for i in range(len(atoms)):
        for j in range(i + 1, len(atoms)):
            a1 = atoms[i]
            a2 = atoms[j]

            w1 = weights.get(a1[1], 1.0)
            w2 = weights.get(a2[1], 1.0)

            dx = a1[2] - a2[2]
            dy = a1[3] - a2[3]
            dz = a1[4] - a2[4]
            dist = math.sqrt(dx*dx + dy*dy + dz*dz)

            total_energy += (w1 * w2) / dist

    return total_energy

def test_unauthorized_simulate():
    try:
        resp = requests.post(f"{BASE_URL}/simulate", data=get_pdb_payload())
    except requests.exceptions.ConnectionError:
        pytest.fail("Service is not running on 127.0.0.1:8080")

    assert resp.status_code == 401, f"Expected 401 Unauthorized, got {resp.status_code}. Response: {resp.text}"

def test_simulate_endpoint():
    try:
        resp = requests.post(f"{BASE_URL}/simulate", headers=HEADERS, data=get_pdb_payload(), headers_update={"Content-Type": "text/plain"})
        if 'Content-Type' not in resp.request.headers:
             resp = requests.post(f"{BASE_URL}/simulate", headers=HEADERS, data=get_pdb_payload())
    except requests.exceptions.ConnectionError:
        pytest.fail("Service is not running on 127.0.0.1:8080")

    assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code}. Response: {resp.text}"
    data = resp.json()
    assert "energy" in data, f"Response missing 'energy' field: {data}"

    expected_energy = calculate_expected_energy()
    actual_energy = data["energy"]

    assert math.isclose(actual_energy, expected_energy, rel_tol=1e-5), f"Expected energy {expected_energy}, got {actual_energy}"

def test_compare_endpoint_significant():
    payload = {"energy_old": 150.123456, "energy_new": 150.123467}
    try:
        resp = requests.post(f"{BASE_URL}/compare", headers=HEADERS, json=payload)
    except requests.exceptions.ConnectionError:
        pytest.fail("Service is not running on 127.0.0.1:8080")

    assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code}. Response: {resp.text}"
    data = resp.json()
    assert "significant" in data, f"Response missing 'significant' field: {data}"
    assert data["significant"] is True, f"Expected significant=True for diff > 1e-5, got {data['significant']}"

def test_compare_endpoint_not_significant():
    payload = {"energy_old": 150.123456, "energy_new": 150.123458}
    try:
        resp = requests.post(f"{BASE_URL}/compare", headers=HEADERS, json=payload)
    except requests.exceptions.ConnectionError:
        pytest.fail("Service is not running on 127.0.0.1:8080")

    assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code}. Response: {resp.text}"
    data = resp.json()
    assert "significant" in data, f"Response missing 'significant' field: {data}"
    assert data["significant"] is False, f"Expected significant=False for diff <= 1e-5, got {data['significant']}"