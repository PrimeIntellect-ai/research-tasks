# test_final_state.py

import os
import csv
import re
import subprocess
import tempfile
import requests
import pytest

VIDEO_PATH = "/app/traffic_feed.mp4"
CSV_PATH = "/app/radar_sensors.csv"
LOG_PATH = "/home/user/etl_experiment.log"
SERVER_URL = "http://127.0.0.1:8080/posterior"
AUTH_HEADER = {"X-Auth-Token": "etl-agent-secret"}

@pytest.fixture(scope="session")
def ground_truth():
    """Compute the ground truth posteriors."""
    assert os.path.isfile(VIDEO_PATH), f"Video missing: {VIDEO_PATH}"
    assert os.path.isfile(CSV_PATH), f"CSV missing: {CSV_PATH}"

    # Read CSV
    priors = {}
    with open(CSV_PATH, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            sec = int(row["timestamp_sec"])
            prior = float(row["prior_prob_speeding"])
            priors[sec] = prior

    # Extract frames and compute max size per second
    # We'll use a temporary directory
    temp_dir = tempfile.mkdtemp()
    try:
        # Extract all frames: frame_%04d.jpg
        cmd = [
            "ffmpeg", "-i", VIDEO_PATH, 
            "-q:v", "2", # Standard high quality to match typical extraction
            os.path.join(temp_dir, "frame_%04d.jpg")
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

        frames = sorted([f for f in os.listdir(temp_dir) if f.startswith("frame_") and f.endswith(".jpg")])

        posteriors = {}
        for sec, prior in priors.items():
            start_idx = sec * 24
            end_idx = (sec + 1) * 24

            sec_frames = frames[start_idx:end_idx]
            if not sec_frames:
                continue

            max_size = 0
            for frame_file in sec_frames:
                size = os.path.getsize(os.path.join(temp_dir, frame_file))
                if size > max_size:
                    max_size = size

            if max_size > 50000:
                ls = 0.8
                lns = 0.4
            else:
                ls = 0.3
                lns = 0.7

            evidence = (ls * prior) + (lns * (1.0 - prior))
            posterior = (ls * prior) / evidence
            posteriors[sec] = {"prior": prior, "posterior": posterior, "max_size": max_size}

        return posteriors
    finally:
        for f in os.listdir(temp_dir):
            os.remove(os.path.join(temp_dir, f))
        os.rmdir(temp_dir)

def test_server_authorized_requests(ground_truth):
    """Test authorized requests to the server."""
    for sec in [0, 5]:
        if sec not in ground_truth:
            continue

        expected_posterior = ground_truth[sec]["posterior"]

        try:
            resp = requests.get(f"{SERVER_URL}?sec={sec}", headers=AUTH_HEADER, timeout=2)
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Failed to connect to server: {e}")

        assert resp.status_code == 200, f"Expected 200 OK for sec={sec}, got {resp.status_code}"

        try:
            actual_posterior = float(resp.text.strip())
        except ValueError:
            pytest.fail(f"Expected float in response body, got: {resp.text}")

        assert abs(actual_posterior - expected_posterior) < 0.001, \
            f"Posterior mismatch for sec={sec}. Expected ~{expected_posterior:.4f}, got {actual_posterior:.4f}"

def test_server_unauthorized_request():
    """Test unauthorized request to the server."""
    try:
        resp = requests.get(f"{SERVER_URL}?sec=0", timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to server: {e}")

    assert resp.status_code == 401, f"Expected 401 Unauthorized, got {resp.status_code}"

def test_experiment_log(ground_truth):
    """Test the experiment log format and contents."""
    assert os.path.isfile(LOG_PATH), f"Log file missing: {LOG_PATH}"

    with open(LOG_PATH, "r") as f:
        log_content = f.read()

    for sec, data in ground_truth.items():
        prior = data["prior"]
        posterior = data["posterior"]

        # Look for [RUN] sec=<sec> prior=<prior> posterior=<posterior>
        # We'll use a regex to allow some formatting flexibility for floats
        pattern = rf"\[RUN\]\s+sec={sec}\s+prior={prior:.1f}0*\s+posterior={posterior:.4f}"

        # If strict match fails, try a more flexible float match
        flexible_pattern = rf"\[RUN\]\s+sec={sec}\s+prior=[0-9.]+\s+posterior={posterior:.4f}"

        match = re.search(flexible_pattern, log_content)
        assert match is not None, f"Could not find matching log entry for sec={sec} with posterior ~{posterior:.4f} in {LOG_PATH}"