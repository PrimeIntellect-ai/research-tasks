# test_final_state.py
import os
import re
import glob
import subprocess
import requests
import time
import pytest

def test_active_mounts():
    """Verify /home/user/active_mounts.txt contains correct mount points."""
    fstab_path = '/app/fstab.mock'
    output_path = '/home/user/active_mounts.txt'

    assert os.path.isfile(output_path), f"Missing {output_path}"

    expected_mounts = []
    if os.path.isfile(fstab_path):
        with open(fstab_path, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 3 and parts[2] in ['ext4', 'xfs']:
                    expected_mounts.append(parts[1])

    with open(output_path, 'r') as f:
        actual_mounts = [line.strip() for line in f if line.strip()]

    assert sorted(actual_mounts) == sorted(expected_mounts), "active_mounts.txt does not contain the correct mount points"

def test_extracted_frames():
    """Verify frames are extracted correctly."""
    frames_dir = '/home/user/data/frames/'
    assert os.path.isdir(frames_dir), f"Directory {frames_dir} does not exist"

    frames = glob.glob(os.path.join(frames_dir, 'frame_*.jpg'))
    assert len(frames) > 0, "No frames extracted"

def get_expected_frame_count():
    video_path = '/app/test_video.mp4'
    if not os.path.isfile(video_path):
        return 0
    cmd = f"ffmpeg -i {video_path} -vf fps=2 -f null - 2>&1 | grep 'frame=' | awk '{{print $2}}'"
    try:
        output = subprocess.check_output(cmd, shell=True, text=True).strip()
        return int(output)
    except:
        return 0

def test_rust_microservice_http():
    """Verify the Rust microservice HTTP responses."""
    url = "http://127.0.0.1:9090/metrics"

    # Test unauthenticated request
    try:
        resp_unauth = requests.get(url, headers={"X-Service-Auth": "wrong-token"}, timeout=2)
        assert resp_unauth.status_code == 401, f"Expected 401 Unauthorized, got {resp_unauth.status_code}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to microservice: {e}")

    # Test authenticated request
    try:
        resp_auth = requests.get(url, headers={"X-Service-Auth": "v1-alpha-xyz"}, timeout=2)
        assert resp_auth.status_code == 200, f"Expected 200 OK, got {resp_auth.status_code}"

        data = resp_auth.json()
        assert data.get("fps") == 2, "JSON response 'fps' should be 2"

        # Verify frame count dynamically
        frames_dir = '/home/user/data/frames/'
        actual_frames = len(glob.glob(os.path.join(frames_dir, 'frame_*.jpg')))
        assert data.get("extracted_frames") == actual_frames, f"JSON 'extracted_frames' should be {actual_frames}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to microservice: {e}")
    except ValueError:
        pytest.fail("Response is not valid JSON")

def test_logrotate_conf():
    """Verify logrotate configuration."""
    conf_path = '/home/user/logrotate.conf'
    assert os.path.isfile(conf_path), f"Missing {conf_path}"

    with open(conf_path, 'r') as f:
        content = f.read()

    assert '/home/user/logs/microservice.log' in content, "Log file path missing in logrotate.conf"
    assert 'size 1M' in content or 'size=1M' in content or '1M' in content, "Size 1M missing in logrotate.conf"
    assert 'rotate 3' in content, "rotate 3 missing in logrotate.conf"
    assert 'compress' in content, "compress missing in logrotate.conf"
    assert 'create 0644 user user' in content or 'create 644 user user' in content, "create permissions missing in logrotate.conf"

def test_run_sh_exists():
    """Verify run.sh exists and is executable."""
    script_path = '/home/user/run.sh'
    assert os.path.isfile(script_path), f"Missing {script_path}"
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable"

def test_microservice_log_exists():
    """Verify microservice.log exists and has entries."""
    log_path = '/home/user/logs/microservice.log'
    assert os.path.isfile(log_path), f"Missing {log_path}"

    with open(log_path, 'r') as f:
        content = f.read()
        assert "GET" in content and "/metrics" in content, "Log file does not contain expected HTTP request entries"