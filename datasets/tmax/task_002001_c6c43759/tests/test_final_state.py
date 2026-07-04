# test_final_state.py
import pytest
import requests
import json
import math

BASE_URL = "http://127.0.0.1:9090"
HEADERS_VALID = {"X-API-Key": "ml-data-secret"}
HEADERS_INVALID = {"X-API-Key": "wrong"}

def get_expected_features(mol_id):
    try:
        from bio_feature_extractor import compute_spectral_gap, local_alignment
    except ImportError:
        pytest.fail("Failed to import bio_feature_extractor. The package was not installed correctly.")

    with open("/home/user/raw_data.json", "r") as f:
        data = json.load(f)

    mol_data = next((item for item in data if item["id"] == mol_id), None)
    if not mol_data:
        pytest.fail(f"Could not find {mol_id} in /home/user/raw_data.json")

    spectral_gap = compute_spectral_gap(mol_data["adj"])
    alignment_score = local_alignment(mol_data["seq"], "GATTACA")

    return spectral_gap, alignment_score

def test_health_valid_auth():
    try:
        resp = requests.get(f"{BASE_URL}/health", headers=HEADERS_VALID, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {BASE_URL}/health: {e}")

    assert resp.status_code == 200, f"Expected 200 OK for /health with valid auth, got {resp.status_code}. Response: {resp.text}"
    try:
        data = resp.json()
    except Exception:
        pytest.fail(f"Response from /health is not valid JSON. Response text: {resp.text}")
    assert data.get("status") == "ok", f"Expected status: ok in /health response, got: {data.get('status')}"

def test_health_invalid_auth():
    try:
        resp = requests.get(f"{BASE_URL}/health", headers=HEADERS_INVALID, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {BASE_URL}/health: {e}")

    assert resp.status_code == 401, f"Expected 401 Unauthorized for /health with invalid auth, got {resp.status_code}. Response: {resp.text}"

def test_health_missing_auth():
    try:
        resp = requests.get(f"{BASE_URL}/health", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {BASE_URL}/health: {e}")

    assert resp.status_code == 401, f"Expected 401 Unauthorized for /health with missing auth, got {resp.status_code}. Response: {resp.text}"

def test_feature_mol_1():
    expected_gap, expected_score = get_expected_features("mol_1")

    try:
        resp = requests.get(f"{BASE_URL}/feature/mol_1", headers=HEADERS_VALID, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {BASE_URL}/feature/mol_1: {e}")

    assert resp.status_code == 200, f"Expected 200 OK for /feature/mol_1, got {resp.status_code}. Response: {resp.text}"
    try:
        data = resp.json()
    except Exception:
        pytest.fail(f"Response from /feature/mol_1 is not valid JSON. Response text: {resp.text}")

    assert data.get("id") == "mol_1", f"Expected id to be 'mol_1', got {data.get('id')}"
    assert "spectral_gap" in data, "Missing 'spectral_gap' in response"
    assert "alignment_score" in data, "Missing 'alignment_score' in response"

    assert math.isclose(data["spectral_gap"], expected_gap, rel_tol=1e-4), f"Expected spectral_gap {expected_gap}, got {data['spectral_gap']}"
    assert math.isclose(data["alignment_score"], expected_score, rel_tol=1e-4), f"Expected alignment_score {expected_score}, got {data['alignment_score']}"

def test_feature_mol_2():
    expected_gap, expected_score = get_expected_features("mol_2")

    try:
        resp = requests.get(f"{BASE_URL}/feature/mol_2", headers=HEADERS_VALID, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {BASE_URL}/feature/mol_2: {e}")

    assert resp.status_code == 200, f"Expected 200 OK for /feature/mol_2, got {resp.status_code}. Response: {resp.text}"
    data = resp.json()

    assert data.get("id") == "mol_2", f"Expected id to be 'mol_2', got {data.get('id')}"
    assert math.isclose(data["spectral_gap"], expected_gap, rel_tol=1e-4), f"Expected spectral_gap {expected_gap}, got {data['spectral_gap']}"
    assert math.isclose(data["alignment_score"], expected_score, rel_tol=1e-4), f"Expected alignment_score {expected_score}, got {data['alignment_score']}"

def test_feature_unknown_mol():
    try:
        resp = requests.get(f"{BASE_URL}/feature/unknown_mol", headers=HEADERS_VALID, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {BASE_URL}/feature/unknown_mol: {e}")

    assert resp.status_code == 404, f"Expected 404 Not Found for /feature/unknown_mol, got {resp.status_code}. Response: {resp.text}"

def test_feature_invalid_auth():
    try:
        resp = requests.get(f"{BASE_URL}/feature/mol_1", headers=HEADERS_INVALID, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {BASE_URL}/feature/mol_1: {e}")

    assert resp.status_code == 401, f"Expected 401 Unauthorized for /feature/mol_1 with invalid auth, got {resp.status_code}. Response: {resp.text}"