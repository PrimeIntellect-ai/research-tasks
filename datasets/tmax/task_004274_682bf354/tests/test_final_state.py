# test_final_state.py

import os
import numpy as np
from scipy.io import wavfile

def test_nginx_conf_exists():
    path = "/home/user/project/nginx.conf"
    assert os.path.isfile(path), f"Nginx config {path} is missing."

def test_api_script_exists():
    path = "/home/user/project/api.py"
    assert os.path.isfile(path), f"API script {path} is missing."

def test_test_script_exists():
    path = "/home/user/project/test_api.py"
    assert os.path.isfile(path), f"Test script {path} is missing."

def test_processed_audio_metric():
    target_file = "/home/user/project/processed_audio.wav"
    assert os.path.isfile(target_file), f"Processed audio file {target_file} is missing. The test script may not have run successfully or saved the output."

    try:
        sample_rate, data = wavfile.read(target_file)
    except Exception as e:
        assert False, f"Failed to read {target_file} as a WAV file: {e}"

    # Handle stereo or mono
    if len(data.shape) > 1:
        data = data[:, 0]

    # Calculate peak amplitude
    peak_amplitude = np.max(np.abs(data.astype(np.float64)))

    # Calculate dBFS (Assuming 16-bit PCM where max is 32768)
    if peak_amplitude == 0:
        dbfs = -100.0
    else:
        dbfs = 20 * np.log10(peak_amplitude / 32768.0)

    # Calculate metric: absolute difference from -3.0 dBFS
    metric = abs(dbfs - (-3.0))
    threshold = 0.1

    assert metric <= threshold, f"Peak volume normalization failed. Expected -3.0 dBFS, got {dbfs:.2f} dBFS (Difference: {metric:.4f} > {threshold})."