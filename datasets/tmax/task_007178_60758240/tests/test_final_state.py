# test_final_state.py

import os
import subprocess

def get_expected_slope():
    """Computes the expected slope using numpy in a subprocess to avoid third-party imports in the test."""
    script = """
import numpy as np

Ns = [10**3, 10**4, 10**5, 10**6, 10**7]
E = []
for N in Ns:
    terms = (1.0 / np.arange(1, N+1, dtype=np.float32)).astype(np.float32)
    s_asc = np.float32(0.0)
    for t in terms: 
        s_asc += t
    s_desc = np.float32(0.0)
    for t in reversed(terms): 
        s_desc += t
    E.append(abs(float(s_asc) - float(s_desc)))

slope, _ = np.polyfit(np.log10(Ns), np.log10(E), 1)
print(f"{slope:.2f}")
"""
    result = subprocess.run(['python3', '-c', script], capture_output=True, text=True, check=True)
    return result.stdout.strip()

def test_script_exists():
    """Check that the error_analysis.py script was created."""
    assert os.path.isfile('/home/user/error_analysis.py'), "/home/user/error_analysis.py does not exist."

def test_slope_file_exists():
    """Check that the slope.txt file was created."""
    assert os.path.isfile('/home/user/slope.txt'), "/home/user/slope.txt does not exist."

def test_slope_value():
    """Check that the computed slope in slope.txt matches the expected empirical value."""
    expected_val = get_expected_slope()

    with open('/home/user/slope.txt', 'r') as f:
        actual_val = f.read().strip()

    assert actual_val == expected_val, f"Expected slope {expected_val}, but got {actual_val} in /home/user/slope.txt. Make sure you are using naive iterative float32 summation."