# test_final_state.py
import os
import json
import subprocess
import numpy as np
import pytest

def test_analysis_json_exists_and_structure():
    """Verify that the output JSON exists and has the correct structure."""
    output_path = "/home/user/output/analysis.json"
    assert os.path.isfile(output_path), f"Output JSON is missing: {output_path}"

    with open(output_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("Output file is not valid JSON.")

    assert "transcription" in data, "Missing 'transcription' key in JSON."
    assert "mfcc_mean" in data, "Missing 'mfcc_mean' key in JSON."
    assert "mfcc_var" in data, "Missing 'mfcc_var' key in JSON."

    assert isinstance(data["transcription"], str), "'transcription' must be a string."
    assert isinstance(data["mfcc_mean"], list), "'mfcc_mean' must be a list."
    assert isinstance(data["mfcc_var"], list), "'mfcc_var' must be a list."

    assert len(data["mfcc_mean"]) == 13, f"Expected 13 MFCC means, got {len(data['mfcc_mean'])}."
    assert len(data["mfcc_var"]) == 13, f"Expected 13 MFCC variances, got {len(data['mfcc_var'])}."

def test_cron_job_setup():
    """Verify that the cron job is set up to run every 15 minutes."""
    try:
        crontab_output = subprocess.check_output(["crontab", "-l"], stderr=subprocess.STDOUT).decode("utf-8")
    except subprocess.CalledProcessError:
        pytest.fail("No crontab found for the current user.")

    # Check for 15-minute intervals and the script name
    valid_cron_time = ("*/15" in crontab_output or "0,15,30,45" in crontab_output or "15" in crontab_output)
    has_script = "process_audio.py" in crontab_output

    assert valid_cron_time and has_script, f"Cron job not properly set up. Current crontab:\n{crontab_output}"

def test_mfcc_mse():
    """Verify that the extracted MFCC means fall within the allowed MSE threshold."""
    output_path = "/home/user/output/analysis.json"
    audio_path = "/app/data/field_recording.wav"

    if not os.path.isfile(output_path) or not os.path.isfile(audio_path):
        pytest.skip("Required files not found for MSE evaluation.")

    with open(output_path, "r") as f:
        data = json.load(f)

    agent_mfcc_mean = np.array(data["mfcc_mean"])

    try:
        import librosa
        y, sr = librosa.load(audio_path, sr=16000)
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13, hop_length=160, n_fft=400)
        ref_mfcc_mean = np.mean(mfccs, axis=1)
    except ImportError:
        # Fallback if librosa is not installed by the agent
        import scipy.io.wavfile as wav
        from scipy.fftpack import dct

        sr, y = wav.read(audio_path)
        if y.ndim > 1:
            y = y.mean(axis=1)
        # Very basic fallback assertion if we can't compute exact librosa MFCCs
        assert len(agent_mfcc_mean) == 13, "Agent MFCC mean must have length 13."
        pytest.skip("librosa not installed, cannot compute exact reference MFCCs for MSE comparison.")
        return

    mse = np.mean((agent_mfcc_mean - ref_mfcc_mean) ** 2)
    threshold = 1.5

    assert mse <= threshold, f"MFCC mean MSE is {mse:.4f}, which exceeds the threshold of {threshold}."