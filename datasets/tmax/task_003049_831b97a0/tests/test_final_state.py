# test_final_state.py
import pytest
import requests
import math

BASE_URL = "http://127.0.0.1:9090"
AUTH_HEADER = {"Authorization": "Bearer MLOPS_SECRET_2024"}

def test_posterior_auth_missing():
    """Test that /posterior requires authorization."""
    try:
        response = requests.get(f"{BASE_URL}/posterior", timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service at {BASE_URL}: {e}")

    assert response.status_code == 401, f"Expected HTTP 401 for missing auth, got {response.status_code}"

def test_posterior_auth_invalid():
    """Test that /posterior rejects invalid authorization."""
    response = requests.get(f"{BASE_URL}/posterior", headers={"Authorization": "Bearer WRONG"}, timeout=2)
    assert response.status_code == 401, f"Expected HTTP 401 for invalid auth, got {response.status_code}"

def test_ingest_schema_enforcement():
    """Test that /ingest enforces schema requirements."""
    # Missing transcript
    response = requests.post(f"{BASE_URL}/ingest", json={"artifact_id": "123"}, timeout=2)
    assert response.status_code == 400, f"Expected HTTP 400 for missing transcript, got {response.status_code}"

    # Missing artifact_id
    response = requests.post(f"{BASE_URL}/ingest", json={"transcript": "test"}, timeout=2)
    assert response.status_code == 400, f"Expected HTTP 400 for missing artifact_id, got {response.status_code}"

    # Empty transcript
    response = requests.post(f"{BASE_URL}/ingest", json={"transcript": "", "artifact_id": "123"}, timeout=2)
    assert response.status_code == 400, f"Expected HTTP 400 for empty transcript, got {response.status_code}"

def test_ingest_and_posterior_logic():
    """Test the Bayesian update logic and posterior calculation."""
    # 1. Ingest a failure (no 'success' in transcript)
    payload_fail = {"transcript": "Failure mode detected", "artifact_id": "092"}
    resp_fail = requests.post(f"{BASE_URL}/ingest", json=payload_fail, timeout=2)
    assert resp_fail.status_code == 200, f"Expected HTTP 200 for valid ingest, got {resp_fail.status_code}"

    data_fail = resp_fail.json()
    assert "alpha" in data_fail and "beta" in data_fail, "Response missing alpha or beta"
    alpha1 = data_fail["alpha"]
    beta1 = data_fail["beta"]

    # 2. Ingest a success ('success' in transcript)
    payload_success = {"transcript": "This was a huge SuCcEsS!", "artifact_id": "093"}
    resp_success = requests.post(f"{BASE_URL}/ingest", json=payload_success, timeout=2)
    assert resp_success.status_code == 200, f"Expected HTTP 200 for valid ingest, got {resp_success.status_code}"

    data_success = resp_success.json()
    alpha2 = data_success["alpha"]
    beta2 = data_success["beta"]

    assert alpha2 == alpha1 + 1, f"Expected alpha to increment by 1, got {alpha2} vs {alpha1}"
    assert beta2 == beta1, f"Expected beta to remain unchanged, got {beta2} vs {beta1}"

    # 3. Check posterior
    resp_post = requests.get(f"{BASE_URL}/posterior", headers=AUTH_HEADER, timeout=2)
    assert resp_post.status_code == 200, f"Expected HTTP 200 for valid auth, got {resp_post.status_code}"

    data_post = resp_post.json()
    assert "expected_success_probability" in data_post, "Response missing expected_success_probability"

    expected_prob = alpha2 / (alpha2 + beta2)
    actual_prob = data_post["expected_success_probability"]
    assert math.isclose(actual_prob, expected_prob, rel_tol=1e-5), f"Expected probability {expected_prob}, got {actual_prob}"