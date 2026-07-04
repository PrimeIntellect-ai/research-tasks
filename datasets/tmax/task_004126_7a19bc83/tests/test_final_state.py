# test_final_state.py
import os
import stat
import subprocess
import hashlib
import requests
import time

def test_filesystem_preparation():
    setup_script = '/home/user/setup_fs.sh'
    launch_script = '/home/user/launch.sh'
    frame_cache = '/home/user/frame_cache'

    assert os.path.isfile(setup_script), f"{setup_script} does not exist."
    assert os.path.isfile(launch_script), f"{launch_script} does not exist."

    assert os.path.isdir(frame_cache), f"{frame_cache} directory does not exist."

    mode = stat.S_IMODE(os.stat(frame_cache).st_mode)
    assert mode == 0o700, f"Permissions of {frame_cache} are {oct(mode)}, expected 0o700."

def test_api_healthcheck():
    url = "http://127.0.0.1:9090/health"
    try:
        response = requests.get(url, timeout=5)
    except requests.RequestException as e:
        assert False, f"Failed to connect to API healthcheck endpoint: {e}"

    assert response.status_code == 200, f"Expected status 200 for /health, got {response.status_code}"
    try:
        data = response.json()
    except ValueError:
        assert False, "Response from /health is not valid JSON."

    assert data.get("status") == "running", f"Expected {{'status': 'running'}}, got {data}"

def test_api_auth_enforcement():
    url = "http://127.0.0.1:9090/frame_hash"
    try:
        response = requests.get(url, timeout=5)
    except requests.RequestException as e:
        assert False, f"Failed to connect to API frame_hash endpoint: {e}"

    assert response.status_code == 401, f"Expected status 401 for unauthorized /frame_hash request, got {response.status_code}"

def test_api_frame_hash_extraction():
    # Compute truth hash
    truth_img = '/tmp/truth_frame_12.jpg'
    cmd = [
        'ffmpeg', '-y', '-ss', '00:00:12', '-i', '/app/dashcam.mp4',
        '-vframes', '1', '-q:v', '2', truth_img
    ]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        assert False, "Failed to run ffmpeg to compute truth hash."

    assert os.path.isfile(truth_img), "Truth frame image was not generated."

    with open(truth_img, 'rb') as f:
        truth_hash = hashlib.sha256(f.read()).hexdigest()

    # Test API
    url = "http://127.0.0.1:9090/frame_hash"
    headers = {"Authorization": "Bearer vault-key-2024"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
    except requests.RequestException as e:
        assert False, f"Failed to connect to API frame_hash endpoint: {e}"

    assert response.status_code == 200, f"Expected status 200 for authorized /frame_hash request, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        assert False, "Response from /frame_hash is not valid JSON."

    assert "hash" in data, "Response JSON does not contain 'hash' key."
    assert data["hash"] == truth_hash, f"Expected hash {truth_hash}, got {data['hash']}."