# test_final_state.py
import os
import subprocess
import sys
import pytest

def test_libsmooth_exists():
    assert os.path.isfile('/home/user/libsmooth.so'), "Shared library /home/user/libsmooth.so is missing."

def test_analyze_script_exists():
    assert os.path.isfile('/home/user/analyze.py'), "Python script /home/user/analyze.py is missing."

def test_result_txt_content():
    assert os.path.isfile('/home/user/result.txt'), "Result file /home/user/result.txt is missing."

    # Compute expected result using a subprocess to avoid importing third-party libs directly in the test file
    script = """
import ctypes
import numpy as np
from sklearn.decomposition import NMF
import os

# Compile smooth.c to a temporary shared library for verification
os.system('gcc -shared -o /tmp/test_libsmooth.so -fPIC /home/user/smooth.c')
lib = ctypes.CDLL('/tmp/test_libsmooth.so')
lib.smooth.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_int]

X = np.loadtxt('/home/user/spectra.csv', delimiter=',')
X_smooth = np.zeros_like(X)

for i in range(X.shape[0]):
    in_ptr = X[i].ctypes.data_as(ctypes.POINTER(ctypes.c_double))
    out_ptr = X_smooth[i].ctypes.data_as(ctypes.POINTER(ctypes.c_double))
    lib.smooth(in_ptr, out_ptr, X.shape[1])

expected_result = ""
for alpha_int in range(11):
    alpha = alpha_int / 10.0
    nmf = NMF(n_components=2, init='random', random_state=42, max_iter=500, solver='cd', alpha_W=alpha, alpha_H=alpha, l1_ratio=1.0)
    nmf.fit(X_smooth)
    if nmf.n_iter_ < 500:
        expected_result = f"alpha={alpha:.1f}, iter={nmf.n_iter_}"
        break
print(expected_result)
"""
    with open('/tmp/compute_expected.py', 'w') as f:
        f.write(script)

    result = subprocess.run([sys.executable, '/tmp/compute_expected.py'], capture_output=True, text=True)
    expected = result.stdout.strip()

    with open('/home/user/result.txt', 'r') as f:
        actual = f.read().strip()

    assert actual == expected, f"Expected result '{expected}', but got '{actual}' in /home/user/result.txt"