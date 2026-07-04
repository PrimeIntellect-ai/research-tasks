# test_final_state.py
import os
import subprocess
import requests
import pytest

def get_actual_frame_count():
    video_path = "/app/surveillance.mp4"
    cmd = [
        "ffprobe", "-v", "error", 
        "-select_streams", "v:0", 
        "-count_packets", 
        "-show_entries", "stream=nb_read_packets", 
        "-of", "csv=p=0", 
        video_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return int(result.stdout.strip())

def test_ssh_config_fixed():
    config_path = os.path.expanduser("~/.ssh/config")
    if not os.path.exists(config_path):
        config_path = "/home/user/.ssh/config"

    assert os.path.isfile(config_path), f"SSH config file {config_path} is missing."
    with open(config_path, "r") as f:
        content = f.read()
    assert "PubkeyAuthentication no" not in content, "SSH config still contains 'PubkeyAuthentication no'."

def test_bashrc_api_port():
    bashrc_path = os.path.expanduser("~/.bashrc")
    if not os.path.exists(bashrc_path):
        bashrc_path = "/home/user/.bashrc"

    assert os.path.isfile(bashrc_path), f"bashrc file {bashrc_path} is missing."
    with open(bashrc_path, "r") as f:
        content = f.read()
    assert "API_PORT=8080" in content.replace(" ", ""), "bashrc does not export API_PORT=8080."

def test_service_unauthorized():
    try:
        response = requests.get("http://127.0.0.1:8080/stats", headers={"Authorization": "Bearer invalid_token"}, timeout=2)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the service on port 8080: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized for invalid token, got {response.status_code}"

def test_service_authorized_and_frame_count():
    expected_frames = get_actual_frame_count()
    token = "secret_token_99x"

    try:
        response = requests.get("http://127.0.0.1:8080/stats", headers={"Authorization": f"Bearer {token}"}, timeout=2)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the service on port 8080: {e}")

    assert response.status_code == 200, f"Expected 200 OK for valid token, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Service did not return valid JSON. Response: {response.text}")

    assert "total_frames" in data, "JSON response missing 'total_frames' key."
    assert data["total_frames"] == expected_frames, f"Expected total_frames to be {expected_frames}, but got {data['total_frames']}"