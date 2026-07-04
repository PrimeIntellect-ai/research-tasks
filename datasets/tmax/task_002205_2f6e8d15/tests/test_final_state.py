# test_final_state.py

import pytest
import requests
import json

def test_api_process_endpoint():
    """
    Test that the HTTP service running on 127.0.0.1:8000/process accepts a PDB payload,
    processes it, and returns the expected JSON structure with mean_dominant_freq and p_value.
    """
    # A minimal PDB string with SEQRES records
    pdb_data = """HEADER    MOCK PDB
SEQRES   1 A   10  ALA CYS ASP GLU PHE GLY HIS ILE LYS LEU
"""

    url = "http://127.0.0.1:8000/process"
    payload = {"pdb_data": pdb_data}

    try:
        response = requests.post(url, json=payload, timeout=45)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to or read from API at {url}. Ensure the service is running. Error: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response body: {response.text}"

    try:
        data = response.json()
    except json.JSONDecodeError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert "mean_dominant_freq" in data, f"Key 'mean_dominant_freq' missing in response: {data}"
    assert "p_value" in data, f"Key 'p_value' missing in response: {data}"

    assert isinstance(data["mean_dominant_freq"], (int, float)), f"mean_dominant_freq must be a number, got {type(data['mean_dominant_freq'])}"
    assert isinstance(data["p_value"], (int, float)), f"p_value must be a number, got {type(data['p_value'])}"

    assert data["mean_dominant_freq"] > 0, f"mean_dominant_freq should be positive, got {data['mean_dominant_freq']}"
    assert 0.0 <= data["p_value"] <= 1.0, f"p_value should be a valid probability between 0 and 1, got {data['p_value']}"