# test_final_state.py
import os
import wave
import struct
import numpy as np
import pytest

def compute_ground_truth(input_path):
    with wave.open(input_path, 'rb') as f:
        frames = f.readframes(f.getnframes())
        input_data = struct.unpack(f'<{f.getnframes()}h', frames)

    input_data = np.array(input_data, dtype=np.float32)
    output_data = np.zeros_like(input_data)

    TAPS = np.array([0.11, 0.22, 0.33, 0.15, -0.05, -0.12, -0.20, -0.04], dtype=np.float32)
    BLOCK_SIZE = 1000

    for start in range(0, len(input_data), BLOCK_SIZE):
        end = min(start + BLOCK_SIZE, len(input_data))
        block = input_data[start:end]
        n = len(block)
        if n <= 0:
            continue

        # Compute mean and variance using float32 to match C++ precision
        mean = np.mean(block, dtype=np.float32)
        variance = np.var(block, dtype=np.float32)
        stddev = np.sqrt(max(0.0001, variance), dtype=np.float32)

        norm_buffer = (block - mean) / stddev

        out_block = np.zeros(n, dtype=np.float32)
        for i in range(n):
            out_val = np.float32(0.0)
            for j in range(8):
                if i - j >= 0:
                    out_val += norm_buffer[i - j] * TAPS[j]
            out_block[i] = out_val

        final_block = (out_block * stddev) + mean
        final_block = np.clip(final_block, -32768.0, 32767.0)

        # Emulate C++ float to int16_t cast (truncation towards zero)
        output_data[start:end] = final_block.astype(np.int16)

    return output_data

def test_output_wav_mse():
    input_path = '/app/audio/input.wav'
    output_path = '/home/user/output.wav'

    assert os.path.exists(output_path), f"Output file {output_path} does not exist."

    try:
        with wave.open(output_path, 'rb') as f:
            frames = f.readframes(f.getnframes())
            agent_data = struct.unpack(f'<{f.getnframes()}h', frames)
            agent_data = np.array(agent_data, dtype=np.float32)
    except Exception as e:
        pytest.fail(f"Failed to read {output_path} as a valid WAV file: {e}")

    truth_data = compute_ground_truth(input_path).astype(np.float32)

    assert len(agent_data) == len(truth_data), f"Output length mismatch: expected {len(truth_data)}, got {len(agent_data)}"

    mse = np.mean((agent_data - truth_data) ** 2)
    threshold = 1e-5

    assert mse <= threshold, f"MSE {mse} exceeds threshold {threshold}. The audio output is not correct."