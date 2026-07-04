# test_final_state.py

import os
import wave
import json
import struct
import pytest
import requests
import re

AUDIO_FILE_PATH = "/app/engine_test_run.wav"
PLOT_FILE_PATH = "/home/user/frame_plot.png"
SERVER_URL = "http://127.0.0.1:8000"

def get_ground_truth_svd():
    # Read wave file
    with wave.open(AUDIO_FILE_PATH, 'rb') as wf:
        n_frames = wf.getnframes()
        raw_data = wf.readframes(n_frames)

    # Convert to float32
    samples = struct.unpack(f"<{n_frames}h", raw_data)
    samples = [s / 32768.0 for s in samples]

    # Reshape to 1024 frames
    frame_size = 1024
    n_rows = len(samples) // frame_size

    # We can use numpy to compute SVD
    import numpy as np
    X = np.array(samples[:n_rows * frame_size], dtype=np.float32).reshape(n_rows, frame_size)
    C = np.dot(X.T, X)

    # SVD
    U, S, Vh = np.linalg.svd(C)

    top_sv = S[0]
    variance_ratio = top_sv / np.sum(S)

    return float(top_sv), float(variance_ratio)

def test_plot_exists_and_valid():
    assert os.path.exists(PLOT_FILE_PATH), f"Plot file missing at {PLOT_FILE_PATH}"
    assert os.path.getsize(PLOT_FILE_PATH) > 1024, "Plot file should be larger than 1KB"
    with open(PLOT_FILE_PATH, 'rb') as f:
        header = f.read(8)
        assert header == b'\x89PNG\r\n\x1a\n', "Plot file is not a valid PNG"

def test_transcript_endpoint():
    try:
        response = requests.get(f"{SERVER_URL}/transcript", timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to {SERVER_URL}/transcript: {e}")

    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    text = response.text.lower()
    text_clean = re.sub(r'[^\w\s]', '', text)
    assert "calibration sequence alpha niner" in text_clean, f"Transcript not found in response: {response.text}"

def test_features_endpoint():
    try:
        response = requests.get(f"{SERVER_URL}/features", timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to {SERVER_URL}/features: {e}")

    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    try:
        data = response.json()
    except json.JSONDecodeError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert "top_singular_value" in data, "Missing top_singular_value in response"
    assert "variance_ratio" in data, "Missing variance_ratio in response"

    gt_top_sv, gt_ratio = get_ground_truth_svd()

    # 1% tolerance
    assert abs(data["top_singular_value"] - gt_top_sv) / gt_top_sv < 0.01, f"Expected top_singular_value near {gt_top_sv}, got {data['top_singular_value']}"
    assert abs(data["variance_ratio"] - gt_ratio) / gt_ratio < 0.01, f"Expected variance_ratio near {gt_ratio}, got {data['variance_ratio']}"

def test_hypothesis_endpoint():
    gt_top_sv, gt_ratio = get_ground_truth_svd()

    # Test 1: threshold below ratio
    thresh1 = gt_ratio - 0.1 if gt_ratio > 0.1 else gt_ratio / 2
    try:
        resp1 = requests.post(f"{SERVER_URL}/hypothesis", json={"threshold": thresh1}, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to {SERVER_URL}/hypothesis: {e}")

    assert resp1.status_code == 200, f"Expected 200, got {resp1.status_code}"
    data1 = resp1.json()
    assert data1.get("reject_null") is True, f"Expected reject_null=true for threshold {thresh1} (ratio is {gt_ratio})"

    # Test 2: threshold above ratio
    thresh2 = gt_ratio + 0.1 if gt_ratio < 0.9 else gt_ratio + (1 - gt_ratio) / 2
    try:
        resp2 = requests.post(f"{SERVER_URL}/hypothesis", json={"threshold": thresh2}, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to {SERVER_URL}/hypothesis: {e}")

    assert resp2.status_code == 200, f"Expected 200, got {resp2.status_code}"
    data2 = resp2.json()
    assert data2.get("reject_null") is False, f"Expected reject_null=false for threshold {thresh2} (ratio is {gt_ratio})"