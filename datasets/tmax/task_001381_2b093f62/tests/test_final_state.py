# test_final_state.py
import os
import subprocess
import numpy as np
from scipy.io import wavfile
import pytest

def test_final_restored_audio_mse():
    """Test that the restored audio file has an MSE <= 0.05 compared to the clean reference."""
    ref_path = '/app/clean_reference.wav'
    test_path = '/home/user/final_restored.wav'

    assert os.path.exists(test_path), f"Output file {test_path} does not exist. Did the cron job run successfully?"
    assert os.path.exists(ref_path), f"Reference file {ref_path} does not exist."

    rate1, data1 = wavfile.read(ref_path)
    rate2, data2 = wavfile.read(test_path)

    assert rate1 == rate2, f"Sample rate mismatch: reference is {rate1}Hz, restored is {rate2}Hz."

    # Convert to float and normalize
    data1 = data1.astype(np.float32) / 32768.0
    data2 = data2.astype(np.float32) / 32768.0

    # Ensure same length
    min_len = min(len(data1), len(data2))
    assert min_len > 0, "One of the audio files is empty."
    data1 = data1[:min_len]
    data2 = data2[:min_len]

    mse = np.mean((data1 - data2)**2)
    assert mse <= 0.05, f"Audio restoration failed: MSE is {mse:.4f}, which is above the threshold of 0.05."

def test_socat_running_and_bound():
    """Test that socat is running and a service is listening on port 9090."""
    try:
        ss_output = subprocess.check_output(['ss', '-tln'], stderr=subprocess.STDOUT).decode()
        assert ':9090 ' in ss_output, "No service is listening on port 9090. Did you set up the socat port forward?"

        ps_output = subprocess.check_output(['ps', 'aux']).decode()
        assert 'socat' in ps_output, "socat process is not running in the background."
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to check network ports or processes: {e}")

def test_cron_job_exists():
    """Test that the cron job for run_restore.sh is set up."""
    try:
        output = subprocess.check_output(['crontab', '-l'], stderr=subprocess.STDOUT).decode()
        assert 'run_restore.sh' in output, "run_restore.sh not found in crontab. Did you schedule the task?"
    except subprocess.CalledProcessError:
        pytest.fail("crontab -l failed or no crontab exists for the user.")

def test_files_exist():
    """Test that all required script, config, and binary files exist."""
    expected_files = [
        "/home/user/restore.cpp",
        "/home/user/filter_config.ini",
        "/home/user/restore_bin",
        "/home/user/run_restore.sh",
        "/home/user/final_restored.wav"
    ]
    for f in expected_files:
        assert os.path.exists(f), f"Expected file {f} is missing."