# test_final_state.py

import os
import subprocess
import pytest
import numpy as np
import scipy.io.wavfile as wavfile

def test_nginx_config_updated():
    path = "/home/user/nginx.conf"
    assert os.path.isfile(path), f"Nginx config file is missing at {path}."
    with open(path, "r") as f:
        content = f.read()
    expected = "proxy_pass http://unix:/home/user/api.sock;"
    assert expected in content, f"Nginx config does not contain the correct upstream socket path. Expected to find '{expected}'."

def test_backend_script_updated():
    path = "/home/user/start_backend.sh"
    assert os.path.isfile(path), f"Backend startup script is missing at {path}."
    with open(path, "r") as f:
        content = f.read()
    assert "TZ=Europe/Paris" in content, "The environment variable TZ=Europe/Paris is not set in the backend startup script."
    assert "LC_ALL=fr_FR.UTF-8" in content, "The environment variable LC_ALL=fr_FR.UTF-8 is not set in the backend startup script."

def test_crontab_configured():
    try:
        output = subprocess.check_output(["crontab", "-l"]).decode("utf-8")
    except subprocess.CalledProcessError:
        pytest.fail("Failed to list crontab. Is it configured?")

    expected_cron = "0 * * * * /home/user/cleanup.sh"
    assert expected_cron in output, f"Crontab does not contain the expected scheduled task. Expected to find '{expected_cron}'."

def test_cleanup_script_exists():
    path = "/home/user/cleanup.sh"
    assert os.path.isfile(path), f"Cleanup script is missing at {path}."

def test_audio_processing_metric():
    processed_file = "/home/user/processed_audio.wav"
    original_file = "/app/voicemail.wav"
    golden_file = "/tmp/golden_reference.wav"

    assert os.path.isfile(processed_file), f"Processed audio file is missing at {processed_file}."
    assert os.path.isfile(original_file), f"Original audio file is missing at {original_file}."

    # Generate golden reference
    cmd = [
        "ffmpeg", "-y", "-i", original_file,
        "-ar", "8000", "-ac", "1", "-af", "lowpass=f=3000",
        golden_file
    ]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to generate golden reference audio: {e.stderr.decode()}")

    # Compute MSE
    try:
        rate1, data1 = wavfile.read(processed_file)
    except Exception as e:
        pytest.fail(f"Failed to read processed audio file: {e}")

    try:
        rate2, data2 = wavfile.read(golden_file)
    except Exception as e:
        pytest.fail(f"Failed to read golden reference audio file: {e}")

    assert rate1 == rate2, f"Sample rate mismatch: processed file is {rate1}Hz, expected {rate2}Hz."

    min_len = min(len(data1), len(data2))
    d1 = data1[:min_len].astype(np.float32)
    d2 = data2[:min_len].astype(np.float32)

    mse = np.mean((d1 - d2)**2)
    threshold = 10.0

    assert mse <= threshold, f"Audio processing failed metric check: MSE is {mse:.4f}, which is > threshold {threshold}."

def test_api_response_exists():
    path = "/home/user/api_response.txt"
    assert os.path.isfile(path), f"API response file is missing at {path}. The pipeline test was likely not completed."