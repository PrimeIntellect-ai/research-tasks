# test_final_state.py
import requests

def verify_response_format(data, expected_frame):
    assert "frame" in data, "Response missing 'frame' key"
    assert "wasserstein" in data, "Response missing 'wasserstein' key"
    assert "p_value" in data, "Response missing 'p_value' key"
    assert "stable" in data, "Response missing 'stable' key"

    assert data["frame"] == expected_frame, f"Expected frame {expected_frame}, got {data['frame']}"
    assert isinstance(data["wasserstein"], float), "wasserstein should be a float"
    assert isinstance(data["p_value"], float), "p_value should be a float"
    assert isinstance(data["stable"], bool), "stable should be a boolean"

def test_frame_0():
    try:
        response = requests.get("http://127.0.0.1:8080/profile/0", timeout=5)
    except requests.exceptions.RequestException as e:
        assert False, f"Failed to connect to the web service: {e}"

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"
    data = response.json()
    verify_response_format(data, 0)
    assert data["stable"] is False, f"Frame 0 is anomalous and should be unstable. Response: {data}"

def test_frame_5():
    try:
        response = requests.get("http://127.0.0.1:8080/profile/5", timeout=5)
    except requests.exceptions.RequestException as e:
        assert False, f"Failed to connect to the web service: {e}"

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"
    data = response.json()
    verify_response_format(data, 5)
    assert data["stable"] is True, f"Frame 5 is stable and should be true. Response: {data}"

def test_frame_10():
    try:
        response = requests.get("http://127.0.0.1:8080/profile/10", timeout=5)
    except requests.exceptions.RequestException as e:
        assert False, f"Failed to connect to the web service: {e}"

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"
    data = response.json()
    verify_response_format(data, 10)
    assert data["stable"] is False, f"Frame 10 is anomalous and should be unstable. Response: {data}"