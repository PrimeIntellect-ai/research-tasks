# test_final_state.py

import os
import sys
import time
import importlib.util
import pytest
import numpy as np
import scipy.io.wavfile as wav

def load_module_from_path(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

def test_files_exist():
    """Verify that the required files have been created."""
    assert os.path.exists("/home/user/libfilter.so"), "Compiled C library /home/user/libfilter.so is missing."
    assert os.path.exists("/home/user/fast_filter.py"), "Python wrapper /home/user/fast_filter.py is missing."
    assert os.path.exists("/home/user/benchmark.py"), "Benchmark script /home/user/benchmark.py is missing."
    assert os.path.exists("/home/user/benchmark_results.txt"), "Benchmark results /home/user/benchmark_results.txt is missing."

def test_performance_and_accuracy():
    """Evaluate the fast_convolve function for accuracy and speedup."""
    # Ensure modules can be loaded
    assert os.path.exists("/home/user/slow_filter.py"), "slow_filter.py is missing."
    assert os.path.exists("/home/user/fast_filter.py"), "fast_filter.py is missing."

    try:
        slow_module = load_module_from_path("slow_filter", "/home/user/slow_filter.py")
        slow_convolve = slow_module.slow_convolve
    except Exception as e:
        pytest.fail(f"Failed to load slow_convolve from slow_filter.py: {e}")

    try:
        fast_module = load_module_from_path("fast_filter", "/home/user/fast_filter.py")
        fast_convolve = fast_module.fast_convolve
    except Exception as e:
        pytest.fail(f"Failed to load fast_convolve from fast_filter.py: {e}")

    # Load audio data
    audio_path = "/app/test_signal.wav"
    assert os.path.exists(audio_path), f"Audio fixture {audio_path} is missing."

    rate, data = wav.read(audio_path)
    # Normalize to float32
    signal = (data / 32768.0).astype(np.float32).tolist()
    kernel = [1.0 / 500.0] * 500

    # To avoid the test taking multiple minutes, we can test on a subset of the signal for the benchmark,
    # but to be faithful to the prompt, we will use the full signal. 
    # If the signal is too large, we cap it to 200,000 samples to keep test times reasonable while still
    # providing a large enough N to measure accurate speedup.
    MAX_SAMPLES = 200000
    if len(signal) > MAX_SAMPLES:
        signal = signal[:MAX_SAMPLES]

    # Measure slow implementation
    t0 = time.time()
    res_slow = slow_convolve(signal, kernel)
    t_slow = time.time() - t0

    # Measure fast implementation
    t0 = time.time()
    try:
        res_fast = fast_convolve(signal, kernel)
    except Exception as e:
        pytest.fail(f"fast_convolve raised an exception during execution: {e}")
    t_fast = time.time() - t0

    # Calculate metrics
    res_slow_arr = np.array(res_slow, dtype=np.float32)
    res_fast_arr = np.array(res_fast, dtype=np.float32)

    assert len(res_slow_arr) == len(res_fast_arr), f"Output length mismatch: expected {len(res_slow_arr)}, got {len(res_fast_arr)}"

    mse = np.mean((res_slow_arr - res_fast_arr) ** 2)
    speedup = t_slow / t_fast if t_fast > 0 else float('inf')

    assert mse < 1e-5, f"Accuracy metric failed: MSE={mse} is not < 1e-5"
    assert speedup >= 50.0, f"Performance metric failed: Speedup={speedup:.2f}x is not >= 50.0x"