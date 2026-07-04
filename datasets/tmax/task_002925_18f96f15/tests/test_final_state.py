# test_final_state.py

import os
import subprocess
import requests
import pytest

BASE_URL = "http://127.0.0.1:9090"
AUTH_HEADER = {"Authorization": "Bearer GraphOrgSecret"}

def get_expected_digest(uris):
    input_data = "\n".join(uris)
    if uris:
        input_data += "\n"

    result = subprocess.run(
        ["/app/dataset_hasher"],
        input=input_data.encode("utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True
    )
    return result.stdout.decode("utf-8").strip()

def test_unauthorized_missing_header():
    """Test that a request without the Authorization header returns 401."""
    response = requests.get(
        f"{BASE_URL}/api/search",
        params={
            "author": "http://example.org/researcher1",
            "domain": "http://example.org/domain1"
        }
    )
    assert response.status_code == 401, f"Expected 401 Unauthorized, got {response.status_code}"

def test_unauthorized_wrong_header():
    """Test that a request with an incorrect Authorization header returns 401."""
    response = requests.get(
        f"{BASE_URL}/api/search",
        params={
            "author": "http://example.org/researcher1",
            "domain": "http://example.org/domain1"
        },
        headers={"Authorization": "Bearer WrongSecret"}
    )
    assert response.status_code == 401, f"Expected 401 Unauthorized, got {response.status_code}"

def test_successful_search():
    """Test a valid search request with correct auth and parameters."""
    response = requests.get(
        f"{BASE_URL}/api/search",
        params={
            "author": "http://example.org/researcher1",
            "domain": "http://example.org/domain1"
        },
        headers=AUTH_HEADER
    )

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"

    data = response.json()
    assert "results" in data, "Response JSON missing 'results' key"
    assert "digest" in data, "Response JSON missing 'digest' key"

    expected_results = [
        "http://example.org/datasetA",
        "http://example.org/datasetB"
    ]

    assert data["results"] == expected_results, f"Expected results {expected_results}, got {data['results']}"

    # Calculate the expected digest using the binary
    # The requirement says: "Pass the sorted URIs (separated by a newline \n) to the standard input"
    input_str = "\n".join(expected_results)

    result = subprocess.run(
        ["/app/dataset_hasher"],
        input=input_str.encode("utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True
    )
    expected_digest = result.stdout.decode("utf-8").strip()

    assert data["digest"] == expected_digest, f"Expected digest {expected_digest}, got {data['digest']}"

def test_empty_search():
    """Test a valid search request that returns no results."""
    response = requests.get(
        f"{BASE_URL}/api/search",
        params={
            "author": "http://example.org/nonexistent",
            "domain": "http://example.org/domain1"
        },
        headers=AUTH_HEADER
    )

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"

    data = response.json()
    assert "results" in data, "Response JSON missing 'results' key"
    assert "digest" in data, "Response JSON missing 'digest' key"

    assert data["results"] == [], f"Expected empty results, got {data['results']}"

    result = subprocess.run(
        ["/app/dataset_hasher"],
        input=b"",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True
    )
    expected_digest = result.stdout.decode("utf-8").strip()

    assert data["digest"] == expected_digest, f"Expected digest {expected_digest}, got {data['digest']}"