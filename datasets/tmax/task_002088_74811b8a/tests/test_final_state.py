# test_final_state.py
import requests
import pytest

BASE_URL = "http://127.0.0.1:9090"

@pytest.mark.parametrize("frame_id", range(10))
def test_pca_endpoint_valid_frames(frame_id):
    url = f"{BASE_URL}/api/pca/{frame_id}"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 for frame {frame_id}, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response from {url} is not valid JSON. Content: {response.text}")

    expected_keys = {"frame_id", "pc1", "pc2", "reconstruction_error"}
    assert expected_keys.issubset(data.keys()), f"Missing keys in response. Expected {expected_keys}, got {list(data.keys())}"

    assert data["frame_id"] == frame_id, f"Expected frame_id {frame_id}, got {data['frame_id']}"

    assert isinstance(data["pc1"], (int, float)), f"pc1 must be numeric, got {type(data['pc1'])}"
    assert isinstance(data["pc2"], (int, float)), f"pc2 must be numeric, got {type(data['pc2'])}"

    recon_err = data["reconstruction_error"]
    assert isinstance(recon_err, (int, float)), f"reconstruction_error must be numeric, got {type(recon_err)}"
    assert recon_err >= 0.0, f"Reconstruction error must be >= 0, got {recon_err}"