# test_final_state.py
import os
import requests
import pytest

def test_vector_store_db_exists():
    assert os.path.isfile("/app/processed/vector_store.db"), "/app/processed/vector_store.db is missing"

def test_benchmark_txt_exists():
    assert os.path.isfile("/app/processed/benchmark.txt"), "/app/processed/benchmark.txt is missing"

def test_frames_extracted():
    for i in range(10):
        frame_path = f"/app/processed/frames/frame_{i}.jpg"
        assert os.path.isfile(frame_path), f"Extracted frame {frame_path} is missing"

def test_api_unauthorized():
    url = "http://127.0.0.1:8080/search?vector=0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized without token, got {response.status_code}"

def test_api_authorized_search():
    url = "http://127.0.0.1:8080/search?vector=0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5"
    headers = {"Authorization": "Bearer ds-api-token"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API: {e}")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Response text: {response.text}")

    assert "timestamp" in data, "Response JSON missing 'timestamp' key"
    assert "event_name" in data, "Response JSON missing 'event_name' key"
    assert "camera_id" in data, "Response JSON missing 'camera_id' key"