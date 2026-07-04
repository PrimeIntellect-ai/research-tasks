# test_final_state.py

import os
import glob
import json
import subprocess
import requests
import pytest

def get_frame_brightnesses(video_path):
    """Extract frames at 1fps and calculate their average grayscale brightness."""
    # Ensure temp dir exists
    os.makedirs("/tmp/test_frames", exist_ok=True)

    # Clear temp dir
    for f in glob.glob("/tmp/test_frames/*.jpg"):
        os.remove(f)

    # Extract frames
    subprocess.run([
        "ffmpeg", "-y", "-i", video_path, "-vf", "fps=1", 
        "/tmp/test_frames/frame_%04d.jpg"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    frames = sorted(glob.glob("/tmp/test_frames/*.jpg"))
    brightnesses = []

    for frame in frames:
        result = subprocess.run([
            "convert", frame, "-colorspace", "gray", "-format", "%[fx:mean*255]", "info:"
        ], capture_output=True, text=True, check=True)
        brightnesses.append(float(result.stdout.strip()))

    return brightnesses

def calculate_expected_posterior(prior, threshold, brightnesses):
    p_s1 = prior
    for b in brightnesses:
        evidence = 1 if b >= threshold else 0
        if evidence == 1:
            likelihood_s1 = 0.85
            likelihood_s0 = 0.40
        else:
            likelihood_s1 = 0.15
            likelihood_s0 = 0.60

        p_e = (likelihood_s1 * p_s1) + (likelihood_s0 * (1 - p_s1))
        if p_e == 0:
            p_s1 = 0
        else:
            p_s1 = (likelihood_s1 * p_s1) / p_e
    return p_s1

def test_pipeline_script_exists():
    assert os.path.isfile("/home/user/pipeline.sh"), "pipeline.sh is missing"
    assert os.access("/home/user/pipeline.sh", os.X_OK), "pipeline.sh is not executable"

def test_inference_service_unauthorized():
    url = "http://localhost:8080/infer?prior=0.5&threshold=100"

    # No auth
    response = requests.get(url)
    assert response.status_code == 401, "Expected 401 Unauthorized without auth header"

    # Wrong auth
    headers = {"Authorization": "Bearer wrong-token"}
    response = requests.get(url, headers=headers)
    assert response.status_code == 401, "Expected 401 Unauthorized with wrong auth header"

def test_inference_service_success():
    url = "http://localhost:8080/infer?prior=0.5&threshold=100"
    headers = {"Authorization": "Bearer mlops-track-99"}

    response = requests.get(url, headers=headers)
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Body: {response.text}"

    data = response.json()
    assert "final_probability" in data, "Response JSON missing 'final_probability' key"

    # Compute expected
    brightnesses = get_frame_brightnesses("/app/dashcam.mp4")
    expected_prob = calculate_expected_posterior(0.5, 100, brightnesses)

    assert abs(float(data["final_probability"]) - expected_prob) < 0.01, \
        f"Expected probability ~{expected_prob}, got {data['final_probability']}"

def test_experiment_tracking_files():
    # Find the latest run directory
    run_dirs = glob.glob("/home/user/experiments/run_*")
    assert len(run_dirs) > 0, "No experiment tracking directories found in /home/user/experiments/"

    latest_run = max(run_dirs, key=os.path.getmtime)

    config_path = os.path.join(latest_run, "config.txt")
    trace_path = os.path.join(latest_run, "trace.csv")

    assert os.path.isfile(config_path), f"config.txt missing in {latest_run}"
    assert os.path.isfile(trace_path), f"trace.csv missing in {latest_run}"

    with open(trace_path, "r") as f:
        lines = f.readlines()
        assert len(lines) > 1, "trace.csv should have at least a header and one data row"
        assert "," in lines[0], "trace.csv does not appear to be comma-separated"