# test_final_state.py
import wave
import numpy as np
import sqlite3
import os
import pytest

def test_output_signal_mse():
    input_path = '/app/test_signal.wav'
    output_path = '/home/user/output_signal.wav'

    assert os.path.exists(input_path), f"Input fixture {input_path} is missing."
    assert os.path.exists(output_path), f"Agent output {output_path} is missing."

    try:
        with wave.open(input_path, 'rb') as wf:
            frames = wf.readframes(wf.getnframes())
            input_signal = np.frombuffer(frames, dtype=np.int16).astype(np.float32)
    except Exception as e:
        pytest.fail(f"Error reading input fixture: {e}")

    # Reference FIR filter (same coefficients as C code)
    filter_coeffs = np.array([0.1, 0.2, 0.4, 0.2, 0.1], dtype=np.float32)
    ref_output = np.convolve(input_signal, filter_coeffs, mode='full')[:len(input_signal)]

    try:
        with wave.open(output_path, 'rb') as wf:
            frames = wf.readframes(wf.getnframes())
            agent_output = np.frombuffer(frames, dtype=np.int16).astype(np.float32)
    except Exception as e:
        pytest.fail(f"Error reading agent output: {e}")

    assert len(ref_output) == len(agent_output), f"Length mismatch: expected {len(ref_output)}, got {len(agent_output)}"

    mse = np.mean((ref_output - agent_output) ** 2)
    assert mse <= 1e-5, f"MSE {mse} exceeds threshold 1e-5. The output signal does not match the reference convolution."

def test_database_migration():
    db_path = '/home/user/migrated.db'
    assert os.path.exists(db_path), f"Migrated database missing at {db_path}"

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Check if metadata table exists
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='metadata'")
    assert c.fetchone() is not None, "Table 'metadata' does not exist in the migrated database."

    # Check if samples table exists
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='samples'")
    assert c.fetchone() is not None, "Table 'samples' does not exist in the migrated database."

    # Check if there are records in metadata
    c.execute("SELECT COUNT(*) FROM metadata")
    count = c.fetchone()[0]
    assert count >= 1, "No records found in the 'metadata' table."

    # Check if there are records in samples
    c.execute("SELECT COUNT(*) FROM samples")
    count_samples = c.fetchone()[0]
    assert count_samples >= 1, "No records found in the 'samples' table."

    conn.close()