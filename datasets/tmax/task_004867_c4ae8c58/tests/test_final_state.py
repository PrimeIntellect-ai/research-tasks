# test_final_state.py

import pytest
import requests

def test_api_result():
    url = "http://127.0.0.1:8080/api/result"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Response text: {response.text}")

    assert "transcript" in data, "Missing 'transcript' in JSON response"
    transcript = data["transcript"].lower()
    assert "alice" in transcript and "johnson" in transcript, f"Transcript does not seem to contain 'Alice Johnson'. Got: {data['transcript']}"
    assert "berlin" in transcript, f"Transcript does not seem to contain 'Berlin'. Got: {data['transcript']}"

    assert data.get("researcher") == "Alice Johnson", f"Expected researcher 'Alice Johnson', got {data.get('researcher')}"
    assert data.get("location") == "Berlin", f"Expected location 'Berlin', got {data.get('location')}"

    expected_projects = ["Project Alpha", "Project Beta"]
    assert data.get("projects") == expected_projects, f"Expected projects {expected_projects}, got {data.get('projects')}"

    expected_budget = 1250000.0
    assert data.get("total_budget") == expected_budget, f"Expected total_budget {expected_budget}, got {data.get('total_budget')}"