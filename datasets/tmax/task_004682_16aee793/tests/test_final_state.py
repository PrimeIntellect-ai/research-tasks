# test_final_state.py
import os
import subprocess
import sys
import pytest

def get_expected_power():
    script = """
import numpy as np
import h5py

with h5py.File('/home/user/data/signals.h5', 'r') as f:
    signals = f['signals'][:]

window = 0.5 * (1 - np.cos(2 * np.pi * np.arange(1024) / 1023))

sum_val = 0.0
c = 0.0

for s in range(1000):
    sig = signals[s] * window
    X = np.fft.rfft(sig)
    power = np.real(X)**2 + np.imag(X)**2
    for k in range(513):
        y = power[k] - c
        t_val = sum_val + y
        c = (t_val - sum_val) - y
        sum_val = t_val

print(f"Total Power: {sum_val:.6f}")
"""
    try:
        output = subprocess.check_output([sys.executable, "-c", script], text=True)
        return output.strip()
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to compute expected power using numpy/h5py: {e}")

def test_total_power_output():
    output_file = "/home/user/total_power.txt"
    assert os.path.isfile(output_file), f"Output file is missing: {output_file}"

    with open(output_file, 'r') as f:
        actual_content = f.read().strip()

    expected_content = get_expected_power()

    assert actual_content == expected_content, (
        f"Contents of {output_file} do not match the expected output.\n"
        f"Expected: '{expected_content}'\n"
        f"Actual:   '{actual_content}'"
    )

def test_mean_spectrum_plot_exists():
    plot_file = "/home/user/mean_spectrum.png"
    assert os.path.isfile(plot_file), f"Plot file is missing: {plot_file}"

    # Check PNG magic number
    with open(plot_file, 'rb') as f:
        header = f.read(8)
    assert header == b'\x89PNG\r\n\x1a\n', f"File {plot_file} is not a valid PNG image."