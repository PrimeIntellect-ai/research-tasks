# test_final_state.py

import os
import math
import re
import pytest

def fft(x):
    N = len(x)
    if N <= 1:
        return x
    even = fft(x[0::2])
    odd = fft(x[1::2])
    T = [complex(math.cos(-2 * math.pi * k / N), math.sin(-2 * math.pi * k / N)) * odd[k] for k in range(N // 2)]
    return [even[k] + T[k] for k in range(N // 2)] + [even[k] - T[k] for k in range(N // 2)]

def compute_truth():
    seq_path = "/home/user/sequence.txt"
    if not os.path.exists(seq_path):
        return None, None

    with open(seq_path, 'r') as f:
        seq = f.read().strip()[:1024]

    mapping = {'A': 1.0, 'C': 2.0, 'G': 3.0, 'T': 4.0}
    if any(c not in mapping for c in seq):
        return None, None

    arr = [mapping[c] for c in seq]

    def get_max_mag(data):
        f = fft(data)
        mags = [abs(c) for c in f[1:513]]
        return max(mags)

    m_orig = get_max_mag(arr)

    seed = 42
    def my_rand():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) & 0x7fffffff
        return seed

    K = 0
    # Monte carlo
    for _ in range(1000):
        for i in range(1023, 0, -1):
            j = my_rand() % (i + 1)
            arr[i], arr[j] = arr[j], arr[i]

        sim_mag = get_max_mag(arr)
        # Using a small epsilon for floating point comparison robustness
        if sim_mag >= m_orig - 1e-9:
            K += 1

    p_val = K / 1000.0
    return m_orig, p_val

def test_fftw_installed():
    """Check if FFTW3 was compiled and installed in the correct prefix."""
    lib_dir = "/home/user/fftw_install/lib"
    assert os.path.isdir(lib_dir), f"FFTW3 library directory not found at {lib_dir}"

    lib_a = os.path.join(lib_dir, "libfftw3.a")
    lib_so = os.path.join(lib_dir, "libfftw3.so")

    assert os.path.isfile(lib_a) or os.path.isfile(lib_so), \
        f"Neither libfftw3.a nor libfftw3.so found in {lib_dir}"

def test_analyze_c_exists():
    """Check if the analyze.c source file exists."""
    src_path = "/home/user/analyze.c"
    assert os.path.isfile(src_path), f"Source file {src_path} is missing."

def test_results_log():
    """Check if results.log exists and contains the correct output."""
    log_path = "/home/user/results.log"
    assert os.path.isfile(log_path), f"Results log {log_path} is missing."

    with open(log_path, 'r') as f:
        content = f.read().strip()

    expected_m_orig, expected_p_val = compute_truth()
    assert expected_m_orig is not None, "Could not compute truth due to missing or invalid sequence.txt"

    # Check format
    match = re.search(r"Max_Mag:\s*([0-9.]+),\s*P-value:\s*([0-9.]+)", content)
    assert match is not None, f"results.log format is incorrect. Found: '{content}'"

    m_orig_str, p_val_str = match.groups()
    m_orig_actual = float(m_orig_str)
    p_val_actual = float(p_val_str)

    expected_m_orig_rounded = round(expected_m_orig, 2)
    expected_p_val_rounded = round(expected_p_val, 3)

    assert math.isclose(m_orig_actual, expected_m_orig_rounded, abs_tol=0.011), \
        f"Expected Max_Mag ~{expected_m_orig_rounded}, but got {m_orig_actual}"

    assert math.isclose(p_val_actual, expected_p_val_rounded, abs_tol=0.0011), \
        f"Expected P-value ~{expected_p_val_rounded}, but got {p_val_actual}"