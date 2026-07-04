# test_final_state.py
import os
import time
import ctypes
import pytest
import numpy as np
from scipy.io import wavfile

def test_final_state():
    lib_path = '/home/user/pr_workspace/librms.so'
    assert os.path.isfile(lib_path), f"{lib_path} is missing. The Makefile was not fixed or run correctly."

    output_path = '/home/user/output.npy'
    assert os.path.isfile(output_path), f"{output_path} is missing. The Python wrapper script did not save the output."

    # Load librms
    try:
        lib = ctypes.CDLL(lib_path)
    except Exception as e:
        pytest.fail(f"Failed to load {lib_path}: {e}")

    # Set up C function signature
    # void compute_rms(const float* input, int num_samples, int window_size, float* output)
    try:
        lib.compute_rms.argtypes = [
            np.ctypeslib.ndpointer(dtype=np.float32, ndim=1, flags='C_CONTIGUOUS'),
            ctypes.c_int,
            ctypes.c_int,
            np.ctypeslib.ndpointer(dtype=np.float32, ndim=1, flags='C_CONTIGUOUS')
        ]
        lib.compute_rms.restype = None
    except AttributeError:
        pytest.fail("Function 'compute_rms' not found in librms.so")

    # Load the audio file
    audio_path = '/app/sample.wav'
    assert os.path.isfile(audio_path), f"{audio_path} is missing."
    sample_rate, data = wavfile.read(audio_path)

    # Convert to float32 as expected by the C function
    data = data.astype(np.float32)
    num_samples = len(data)
    window_size = 1024

    output = np.zeros_like(data, dtype=np.float32)

    # Measure execution time
    start_time = time.perf_counter()
    lib.compute_rms(data, num_samples, window_size, output)
    end_time = time.perf_counter()

    execution_time = end_time - start_time

    # Assert performance threshold
    assert execution_time <= 0.05, f"Execution time {execution_time:.4f}s exceeds threshold of 0.05s. The C implementation is likely still O(N*W)."

    # Load the student's saved output
    try:
        student_output = np.load(output_path)
    except Exception as e:
        pytest.fail(f"Failed to load {output_path}: {e}")

    assert student_output.shape == output.shape, f"Shape mismatch: saved output has shape {student_output.shape}, expected {output.shape}"

    # Ensure the C implementation produces consistent results with the saved output
    mse = np.mean((student_output - output) ** 2)
    assert mse < 1e-5, f"MSE between C output and saved output.npy is {mse:.6e}, expected < 1e-5"

    # Basic sanity check to ensure the output isn't trivially zero
    assert np.max(output) > 0.0, "The computed RMS output is entirely zeros, indicating a flawed algorithm."