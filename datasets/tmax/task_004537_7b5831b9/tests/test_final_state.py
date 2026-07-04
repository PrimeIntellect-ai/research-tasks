# test_final_state.py
import requests

def test_anomaly_endpoint():
    url = "http://127.0.0.1:8888/anomaly"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        assert False, f"Failed to connect to {url} or request timed out: {e}"

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}. Response body: {response.text}"

    try:
        data = response.json()
    except ValueError:
        assert False, f"Response body is not valid JSON: {response.text}"

    assert "frame" in data, f"JSON response is missing the 'frame' key. Got: {data}"
    assert data["frame"] == 50, f"Expected frame number to be 50, but got {data['frame']}"