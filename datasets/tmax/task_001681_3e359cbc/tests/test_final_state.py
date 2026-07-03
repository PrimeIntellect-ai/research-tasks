# test_final_state.py
import os
import requests
import pytest

BASE_URL = "http://127.0.0.1:8080"

def test_unauthorized_trigger():
    """Verify that triggering the pipeline without the correct auth header fails."""
    try:
        response = requests.post(f"{BASE_URL}/trigger_pipeline", timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail("Could not connect to the Flask app on 127.0.0.1:8080. Is it running?")

    assert response.status_code == 401, f"Expected 401 Unauthorized for missing auth, got {response.status_code}. Response: {response.text}"

def test_authorized_trigger_and_data_verification():
    """Verify the full pipeline execution and the correctly processed outputs."""
    # 1. Trigger the pipeline with correct auth
    headers = {"Authorization": "Bearer loc-token-99"}
    try:
        response = requests.post(f"{BASE_URL}/trigger_pipeline", headers=headers, timeout=15)
    except requests.exceptions.ConnectionError:
        pytest.fail("Could not connect to the Flask app on 127.0.0.1:8080. Is it running?")

    assert response.status_code == 200, f"Expected 200 OK for authorized trigger, got {response.status_code}. Response: {response.text}"

    # Verify the output file was created by the pipeline
    assert os.path.isfile("/home/user/processed_metrics.json"), "/home/user/processed_metrics.json was not created after triggering the pipeline."

    # 2. Verify ES forward fill logic
    resp_es = requests.get(f"{BASE_URL}/report?lang=es&hour=2023-10-01T03:00:00Z", timeout=5)
    assert resp_es.status_code == 200, f"Expected 200 OK for ES report, got {resp_es.status_code}. Response: {resp_es.text}"

    try:
        data_es = resp_es.json()
    except ValueError:
        pytest.fail(f"Expected JSON response for ES report, got: {resp_es.text}")

    assert data_es.get("strings_translated") == 150, f"ES strings_translated mismatch. Expected 150, got {data_es.get('strings_translated')}"
    assert data_es.get("missing_keys") == 20, f"ES missing_keys mismatch. Expected 20, got {data_es.get('missing_keys')}"
    assert data_es.get("summary_text") == "Estado ES: 150 traducidas, 20 faltantes.", f"ES summary_text mismatch. Got: {data_es.get('summary_text')}"

    # 3. Verify FR backward fill logic
    resp_fr = requests.get(f"{BASE_URL}/report?lang=fr&hour=2023-10-01T00:00:00Z", timeout=5)
    assert resp_fr.status_code == 200, f"Expected 200 OK for FR report, got {resp_fr.status_code}. Response: {resp_fr.text}"

    try:
        data_fr = resp_fr.json()
    except ValueError:
        pytest.fail(f"Expected JSON response for FR report, got: {resp_fr.text}")

    assert data_fr.get("strings_translated") == 90, f"FR strings_translated mismatch. Expected 90, got {data_fr.get('strings_translated')}"
    assert data_fr.get("missing_keys") == 40, f"FR missing_keys mismatch. Expected 40, got {data_fr.get('missing_keys')}"
    assert data_fr.get("summary_text") == "Statut FR: 90 traduites, 40 manquantes.", f"FR summary_text mismatch. Got: {data_fr.get('summary_text')}"

def test_report_not_found():
    """Verify that a missing language or hour returns a 404."""
    try:
        resp = requests.get(f"{BASE_URL}/report?lang=de&hour=2023-10-01T00:00:00Z", timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail("Could not connect to the Flask app on 127.0.0.1:8080.")

    assert resp.status_code == 404, f"Expected 404 for missing language/hour, got {resp.status_code}. Response: {resp.text}"