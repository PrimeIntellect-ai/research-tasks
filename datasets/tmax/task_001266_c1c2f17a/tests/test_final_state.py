# test_final_state.py
import requests
import time
import pytest

def test_citation_path_endpoint():
    url = "http://127.0.0.1:8080/citation-path"

    # Wait for the service to be up
    max_retries = 5
    response = None
    for i in range(max_retries):
        try:
            response = requests.get(url, timeout=2)
            break
        except requests.exceptions.RequestException:
            if i == max_retries - 1:
                pytest.fail(f"Failed to connect to {url} after {max_retries} attempts. Ensure the web service is running on 127.0.0.1:8080.")
            time.sleep(1)

    assert response.status_code == 200, f"Expected HTTP status 200, got {response.status_code}"

    content_type = response.headers.get("Content-Type", "")
    assert "application/json" in content_type, f"Expected Content-Type application/json, got {content_type}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail("Response body is not valid JSON.")

    assert data.get("source_id") == 105, f"Expected source_id 105, got {data.get('source_id')}"
    assert data.get("target_id") == 402, f"Expected target_id 402, got {data.get('target_id')}"
    assert data.get("path_length") == 3, f"Expected path_length 3, got {data.get('path_length')}"

    expected_path = [
        {"step": 1, "id": 105, "title": "Graph Theory Basics"},
        {"step": 2, "id": 210, "title": "Advanced Network Analysis"},
        {"step": 3, "id": 315, "title": "Citation Dynamics"},
        {"step": 4, "id": 402, "title": "Predictive Modeling in Academia"}
    ]

    assert data.get("path") == expected_path, f"Expected path {expected_path}, got {data.get('path')}"