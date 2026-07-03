# test_final_state.py
import os
import wave
import numpy as np
import pytest

def read_wav(path):
    with wave.open(path, 'rb') as w:
        frames = w.readframes(w.getnframes())
        return np.frombuffer(frames, dtype=np.int16)

def test_processed_output_exists():
    output_path = "/home/user/processed_output.wav"
    assert os.path.exists(output_path), f"Processed output file {output_path} does not exist. The bash script must generate this file."

def test_audio_mse():
    actual_path = "/home/user/processed_output.wav"
    expected_path = "/app/golden_processed.wav"

    assert os.path.exists(actual_path), f"Output file {actual_path} is missing."
    assert os.path.exists(expected_path), f"Golden file {expected_path} is missing."

    try:
        actual = read_wav(actual_path)
    except Exception as e:
        pytest.fail(f"Failed to read actual output as a WAV file: {e}")

    try:
        expected = read_wav(expected_path)
    except Exception as e:
        pytest.fail(f"Failed to read golden output as a WAV file: {e}")

    # Ensure lengths match or trim to minimum length
    min_len = min(len(actual), len(expected))
    actual = actual[:min_len]
    expected = expected[:min_len]

    if min_len == 0:
        pytest.fail("One of the audio files has 0 frames.")

    mse = np.mean((actual.astype(np.float32) - expected.astype(np.float32)) ** 2)

    assert mse <= 0.001, f"Audio MSE is {mse}, which exceeds the threshold of 0.001. The output audio does not match the expected filter output."