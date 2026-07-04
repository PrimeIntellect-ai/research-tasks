# test_final_state.py
import pytest
import requests
import time

BASE_URL = "http://127.0.0.1:8000"
AUTH_HEADER = {"Authorization": "Bearer ml-data-token-999"}

def wait_for_service():
    """Wait for the FastAPI service to become available."""
    for _ in range(30):
        try:
            requests.get(BASE_URL)
            return True
        except requests.exceptions.ConnectionError:
            time.sleep(1)
    return False

@pytest.fixture(scope="module", autouse=True)
def ensure_service_running():
    assert wait_for_service(), "FastAPI service is not running on 127.0.0.1:8000"

def test_get_features_unauthorized():
    """Test that GET /features without auth returns 401 or 403."""
    response = requests.get(f"{BASE_URL}/features")
    assert response.status_code in [401, 403], f"Expected 401 or 403 without auth, got {response.status_code}"

def test_get_features_authorized():
    """Test GET /features with valid auth returns correct data."""
    response = requests.get(f"{BASE_URL}/features", headers=AUTH_HEADER)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {response.text}"

    data = response.json()
    assert isinstance(data, list), "Expected a JSON list of features"
    assert len(data) == 10, f"Expected 10 frames, got {len(data)}"

    for i in range(10):
        item = data[i]
        assert "frame_index" in item, "Missing 'frame_index' in response"
        assert "mean_intensity" in item, "Missing 'mean_intensity' in response"
        assert "is_bright" in item, "Missing 'is_bright' in response"

        assert item["frame_index"] == i, f"Expected frame_index {i}, got {item['frame_index']}"

        if i < 5:
            assert not item["is_bright"], f"Frame {i} should not be bright"
            assert item["mean_intensity"] < 120.0, f"Frame {i} intensity should be < 120"
        else:
            assert item["is_bright"], f"Frame {i} should be bright"
            assert item["mean_intensity"] >= 120.0, f"Frame {i} intensity should be >= 120"

def test_post_predict_authorized_dark():
    """Test POST /predict for a dark frame."""
    payload = {"frame_index": 2}
    response = requests.post(f"{BASE_URL}/predict", json=payload, headers=AUTH_HEADER)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {response.text}"

    data = response.json()
    assert "predicted_is_bright" in data, "Missing 'predicted_is_bright' in response"
    assert data["predicted_is_bright"] is False, "Expected predicted_is_bright to be False for frame 2"

def test_post_predict_authorized_bright():
    """Test POST /predict for a bright frame."""
    payload = {"frame_index": 8}
    response = requests.post(f"{BASE_URL}/predict", json=payload, headers=AUTH_HEADER)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {response.text}"

    data = response.json()
    assert "predicted_is_bright" in data, "Missing 'predicted_is_bright' in response"
    assert data["predicted_is_bright"] is True, "Expected predicted_is_bright to be True for frame 8"

def test_post_predict_invalid_schema():
    """Test POST /predict with invalid schema returns 422."""
    payload = {"frame": "two"}
    response = requests.post(f"{BASE_URL}/predict", json=payload, headers=AUTH_HEADER)
    assert response.status_code == 422, f"Expected 422 Unprocessable Entity, got {response.status_code}"