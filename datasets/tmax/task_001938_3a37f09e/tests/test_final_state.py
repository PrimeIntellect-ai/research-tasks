# test_final_state.py

import os
import urllib.request
import urllib.error
import numpy as np
import scipy.io.wavfile as wavfile
import pytest

def test_audio_normalization_mse():
    """Test that the processed audio file has an MSE <= 2.0 compared to the ground truth."""
    original_path = "/app/ivr_greeting.wav"
    processed_path = "/home/user/processed_greeting.wav"

    assert os.path.exists(original_path), f"Original audio file {original_path} is missing."
    assert os.path.exists(processed_path), f"Processed audio file {processed_path} is missing."

    rate_orig, data_orig = wavfile.read(original_path)
    data_orig = data_orig.astype(np.float64)

    peak = np.max(np.abs(data_orig))
    if peak == 0:
        target_data = data_orig
    else:
        scaling_factor = 26214.0 / peak
        target_data = np.round(data_orig * scaling_factor).astype(np.int16)

    rate_proc, data_proc = wavfile.read(processed_path)

    assert rate_orig == rate_proc, f"Sample rate mismatch: original {rate_orig}, processed {rate_proc}"
    assert len(target_data) == len(data_proc), f"Length mismatch: expected {len(target_data)}, got {len(data_proc)}"

    mse = np.mean((target_data.astype(np.float64) - data_proc.astype(np.float64)) ** 2)

    assert mse <= 2.0, f"MSE is too high: {mse} (threshold is 2.0)"

def test_health_status_log():
    """Test that the integration verification script generated the correct log file."""
    log_path = "/home/user/health_status.log"
    assert os.path.exists(log_path), f"Log file {log_path} is missing."

    with open(log_path, "r") as f:
        content = f.read().strip()

    assert content == "MIGRATION_READY", f"Expected log content 'MIGRATION_READY', got '{content}'"

def test_health_service_running_on_9090():
    """Test that the health service is listening on port 9090 and returning the correct response."""
    url = "http://127.0.0.1:9090/health"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=2) as response:
            status = response.getcode()
            body = response.read().decode('utf-8').strip()
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to health service at {url}: {e}")

    assert status == 200, f"Expected HTTP 200 from {url}, got {status}"
    assert body == "MIGRATION_READY", f"Expected response 'MIGRATION_READY' from {url}, got '{body}'"

def test_port_forwarding_on_8080():
    """Test that port forwarding is working from port 8080 to the health service."""
    url = "http://127.0.0.1:8080/health"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=2) as response:
            status = response.getcode()
            body = response.read().decode('utf-8').strip()
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to forwarded port at {url}: {e}")

    assert status == 200, f"Expected HTTP 200 from {url}, got {status}"
    assert body == "MIGRATION_READY", f"Expected response 'MIGRATION_READY' from {url}, got '{body}'"