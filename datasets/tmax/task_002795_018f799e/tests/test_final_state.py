# test_final_state.py
import os
import wave
import struct
import pytest

def compute_reference(wav_path):
    with wave.open(wav_path, 'rb') as wf:
        n_frames = wf.getnframes()
        data = wf.readframes(n_frames)
        samples = struct.unpack(f"<{n_frames}h", data)

    cumulative = 0.0
    ref = []
    for s in samples:
        val = s / 32768.0
        cumulative += (val * val)
        ref.append(cumulative)
    return ref

def test_final_output_mse():
    wav_path = '/app/diagnostic_recording.wav'
    output_path = '/home/user/pipeline/final_output.txt'

    assert os.path.exists(output_path), f"Output file missing: {output_path}. Did the pipeline run successfully?"

    ref_data = compute_reference(wav_path)

    agent_data = []
    with open(output_path, 'r') as f:
        for line in f:
            if line.strip():
                try:
                    agent_data.append(float(line))
                except ValueError:
                    pytest.fail(f"Could not parse line as float: '{line.strip()}'. Ensure debug logs are not in stdout.")

    assert len(agent_data) == len(ref_data), f"Length mismatch in {output_path}: expected {len(ref_data)} lines, but got {len(agent_data)} lines."

    mse = sum((a - r)**2 for a, r in zip(agent_data, ref_data)) / len(ref_data)

    threshold = 1e-10
    assert mse <= threshold, f"MSE is too high: {mse} > {threshold}. Double-precision floats and proper formatting are required."