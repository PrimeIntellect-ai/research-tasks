# test_final_state.py

import os
import zipfile
import json
import io
import numpy as np
import scipy.io.wavfile as wavfile
import pytest

def test_safe_extraction():
    extracted_dir = "/home/user/extracted"
    assert os.path.exists(extracted_dir), f"Directory {extracted_dir} does not exist."

    # Check safe files
    assert os.path.exists(os.path.join(extracted_dir, "transmission.wav")), "transmission.wav was not extracted."
    assert os.path.exists(os.path.join(extracted_dir, "metadata.json")), "metadata.json was not extracted."

    # Check malicious files are absent from the system
    assert not os.path.exists("/home/user/evil.txt"), "Malicious file evil.txt was extracted outside the target directory."
    assert not os.path.exists("/etc/passwd_overwrite"), "Malicious file passwd_overwrite was extracted outside the target directory."

    # Check they weren't extracted inside the target dir under sanitized names
    assert not os.path.exists(os.path.join(extracted_dir, "evil.txt")), "Malicious file evil.txt was extracted inside the target directory. It should have been skipped."
    assert not os.path.exists(os.path.join(extracted_dir, "passwd_overwrite")), "Malicious file passwd_overwrite was extracted inside the target directory. It should have been skipped."

def test_audio_processing():
    agent_output = "/home/user/clean_transmission.wav"
    assert os.path.exists(agent_output), f"Agent output file {agent_output} does not exist."

    # Load original data and metadata directly from the zip file to ensure pristine reference
    zip_path = "/app/artifacts.zip"
    with zipfile.ZipFile(zip_path, "r") as zf:
        with zf.open("metadata.json") as f:
            metadata = json.load(f)
        with zf.open("transmission.wav") as f:
            orig_rate, orig_data = wavfile.read(io.BytesIO(f.read()))

    start_sec = metadata["message_start_sec"]
    end_sec = metadata["message_end_sec"]
    window = metadata["smoothing_window"]

    # Calculate crop indices
    start_idx = int(start_sec * orig_rate)
    end_idx = int(end_sec * orig_rate)

    # Crop audio
    cropped_data = orig_data[start_idx:end_idx]

    # Apply moving average filter
    # Using cumsum for efficient moving average calculation over potentially large arrays
    if cropped_data.ndim == 1:
        cumsum = np.cumsum(np.insert(cropped_data.astype(float), 0, 0))
        ref_data = np.zeros_like(cropped_data, dtype=float)
        for i in range(len(cropped_data)):
            start_w = max(0, i - window + 1)
            end_w = i + 1
            ref_data[i] = (cumsum[end_w] - cumsum[start_w]) / (end_w - start_w)
    else:
        # Handle multi-channel audio if present
        cumsum = np.cumsum(np.insert(cropped_data.astype(float), 0, 0, axis=0), axis=0)
        ref_data = np.zeros_like(cropped_data, dtype=float)
        for i in range(len(cropped_data)):
            start_w = max(0, i - window + 1)
            end_w = i + 1
            ref_data[i] = (cumsum[end_w] - cumsum[start_w]) / (end_w - start_w)

    # Load agent data
    agent_rate, agent_data = wavfile.read(agent_output)

    assert agent_rate == orig_rate, f"Agent sample rate {agent_rate} does not match original {orig_rate}."
    assert len(agent_data) == len(ref_data), f"Agent audio length {len(agent_data)} does not match expected {len(ref_data)}."

    # Calculate Mean Squared Error
    mse = np.mean((agent_data.astype(float) - ref_data)**2)

    threshold = 1.0
    assert mse <= threshold, f"MSE {mse:.4f} exceeds threshold of {threshold}. Audio processing (cropping or smoothing) is incorrect."