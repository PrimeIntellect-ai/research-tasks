# test_final_state.py
import os
import time
import wave
import struct
import subprocess
import pytest
import math

def test_session_id_extracted():
    session_file = '/app/session_id.txt'
    assert os.path.exists(session_file), f"{session_file} does not exist."
    with open(session_file, 'r') as f:
        sid = f.read().strip()
    assert "SES-9928-PERF-01" in sid, f"Incorrect Session ID found in {session_file}: '{sid}'"

def test_processor_fixed_exists():
    assert os.path.exists('/app/processor_fixed.cpp'), "/app/processor_fixed.cpp is missing."
    assert os.path.exists('/app/processor_fixed'), "/app/processor_fixed executable is missing."
    assert os.access('/app/processor_fixed', os.X_OK), "/app/processor_fixed is not executable."

def test_performance_and_correctness():
    wav_file = '/app/transmission.wav'
    out_file = '/app/output.bin'

    assert os.path.exists(wav_file), f"Audio fixture {wav_file} is missing."

    # Remove output if it exists to ensure we generate a fresh one
    if os.path.exists(out_file):
        os.remove(out_file)

    # Measure execution time
    start_time = time.time()
    result = subprocess.run(
        ["/app/processor_fixed", wav_file, out_file],
        capture_output=True,
        text=True
    )
    duration = time.time() - start_time

    assert result.returncode == 0, f"Execution failed with return code {result.returncode}. Stderr: {result.stderr}"
    assert os.path.exists(out_file), f"Output file {out_file} was not created."

    # Metric evaluation
    threshold = 0.1
    assert duration <= threshold, f"Runtime metric failed: execution took {duration:.4f}s, which is > threshold {threshold}s"

    # Verify correctness of the output
    with wave.open(wav_file, 'rb') as w:
        nframes = w.getnframes()
        frames = w.readframes(nframes)
        samples = struct.unpack(f'<{nframes}h', frames)

    with open(out_file, 'rb') as f:
        output_data = f.read()

    assert len(output_data) == len(samples), f"Output size mismatch: expected {len(samples)} bytes, got {len(output_data)} bytes."

    # Compute expected output for a small subset to ensure logic is correct
    # The C++ code uses a window size of 1024
    window_size = 1024
    expected_energy = []

    # Just check the first 100 samples to verify correctness without taking too long in python
    for i in range(100):
        sum_sq = 0.0
        count = 0
        for j in range(window_size):
            if i + j < len(samples):
                sum_sq += float(samples[i + j]) * float(samples[i + j])
                count += 1
        energy = math.sqrt(sum_sq / count) if count > 0 else 0.0
        expected_energy.append(energy)

    expected_encoded = []
    prev = 0.0
    for i in range(100):
        diff = expected_energy[i] - prev
        val = max(-128.0, min(127.0, diff))
        expected_encoded.append(int(val))
        prev = expected_energy[i]

    actual_encoded = struct.unpack(f'<{100}b', output_data[:100])

    for i in range(100):
        assert actual_encoded[i] == expected_encoded[i], f"Data mismatch at index {i}: expected {expected_encoded[i]}, got {actual_encoded[i]}"