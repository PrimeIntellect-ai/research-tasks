# test_final_state.py

import json
import math
import os
import struct
import wave
import pytest

def test_hard_links_created():
    """Verify that the hard links are correctly created in the restored directory."""
    expected_links = [
        ("blob_001", "logs/voice_memo_2023.wav"),
        ("blob_002", "etc/sysconfig.txt"),
        ("blob_003", "db/users.sql")
    ]

    for blob_id, original_path in expected_links:
        blob_path = f"/app/blobs/{blob_id}"
        restored_path = f"/app/restored/{original_path}"

        assert os.path.exists(restored_path), f"Restored file {restored_path} is missing."

        # Check if it's a hard link by comparing inodes
        blob_stat = os.stat(blob_path)
        restored_stat = os.stat(restored_path)

        assert blob_stat.st_ino == restored_stat.st_ino, \
            f"File {restored_path} is not a hard link to {blob_path}."

def test_rms_output_mse():
    """Verify that the RMS output has an MSE < 1e-5 compared to the true RMS."""
    output_path = "/app/restored/rms_output.json"
    assert os.path.exists(output_path), f"Output file {output_path} is missing."

    with open(output_path, 'r') as f:
        try:
            agent_rms = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {output_path} is not valid JSON.")

    assert isinstance(agent_rms, list), "Output JSON must be an array."

    fixture_path = "/app/blobs/blob_001"
    assert os.path.exists(fixture_path), f"Fixture file {fixture_path} missing."

    with wave.open(fixture_path, 'rb') as wav:
        frames = wav.readframes(wav.getnframes())
        sample_rate = wav.getframerate()
        channels = wav.getnchannels()
        sampwidth = wav.getsampwidth()

    fmt = "<" + "h" * (len(frames) // 2)
    samples = struct.unpack(fmt, frames)

    mono_samples = []
    for i in range(0, len(samples), channels):
        mono_samples.append(samples[i] / 32768.0)

    window_size = int(sample_rate * 0.1)
    true_rms = []
    for i in range(0, len(mono_samples), window_size):
        window = mono_samples[i:i+window_size]
        if len(window) < window_size:
            window = list(window) + [0.0] * (window_size - len(window))

        sq_sum = sum(x*x for x in window)
        true_rms.append(math.sqrt(sq_sum / window_size))

    assert len(agent_rms) == len(true_rms), \
        f"Length mismatch: agent output has {len(agent_rms)} values, expected {len(true_rms)}."

    mse = sum((a - t)**2 for a, t in zip(agent_rms, true_rms)) / len(true_rms)

    assert mse < 1e-5, f"MSE {mse} exceeds threshold of 1e-5."