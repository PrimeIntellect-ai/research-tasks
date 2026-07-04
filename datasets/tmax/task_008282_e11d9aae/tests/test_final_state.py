# test_final_state.py

import os
import subprocess
import json
import pytest

def test_script_exists():
    """Check if the preparation script exists."""
    script_path = "/home/user/prepare_features.py"
    assert os.path.isfile(script_path), f"Expected script {script_path} does not exist."

def test_hdf5_file_exists():
    """Check if the output HDF5 file was created."""
    h5_path = "/home/user/data/features.h5"
    assert os.path.isfile(h5_path), f"Expected output file {h5_path} does not exist."

def test_hdf5_contents():
    """Verify the contents of the HDF5 file using a subprocess to avoid third-party imports in the test."""
    h5_path = "/home/user/data/features.h5"

    # We use a small python script to read the HDF5 file and output its metadata and values as JSON.
    # This avoids directly importing numpy and h5py in the pytest file, adhering to stdlib-only rules.
    checker_script = f"""
import sys
import json
try:
    import h5py
    import numpy as np
except ImportError:
    print("MISSING_MODULES")
    sys.exit(0)

try:
    with h5py.File('{h5_path}', 'r') as f:
        data = {{}}
        for key in f.keys():
            ds = f[key]
            data[key] = {{
                "dtype": str(ds.dtype),
                "shape": list(ds.shape),
                "values": ds[:].tolist()
            }}
        print(json.dumps(data))
except Exception as e:
    print("ERROR:", str(e))
    sys.exit(1)
"""
    result = subprocess.run(["python3", "-c", checker_script], capture_output=True, text=True)
    assert result.returncode == 0, f"Failed to read HDF5 file. Error: {result.stderr}"

    output = result.stdout.strip()
    assert not output.startswith("ERROR:"), f"Error reading HDF5: {output}"
    assert output != "MISSING_MODULES", "h5py or numpy is not installed in the environment."

    try:
        data = json.loads(output)
    except json.JSONDecodeError:
        pytest.fail(f"Failed to parse checker output: {output}")

    expected_keys = ["seq1", "seq2", "seq3"]
    for key in expected_keys:
        assert key in data, f"Dataset '{key}' is missing from the HDF5 file."
        assert data[key]["dtype"] == "float64", f"Dataset '{key}' should have dtype float64, got {data[key]['dtype']}."

    # Recompute expected FFT magnitudes
    import cmath

    def compute_fft_magnitude(seq):
        n = len(seq)
        out = []
        for k in range(n):
            real = 0.0
            imag = 0.0
            for t in range(n):
                angle = -2j * cmath.pi * k * t / n
                val = seq[t] * cmath.exp(angle)
                real += val.real
                imag += val.imag
            out.append(abs(complex(real, imag)))
        return out

    seq1_mapped = [1., 4., 3., 2., 3., 4., 1., 2., 3., 4., 1., 3., 2., 4., 1., 3.]
    seq2_mapped = [3., 3., 3., 2., 2., 2., 1., 1., 1., 4., 4., 4.]
    seq3_mapped = [1., 0., 0., 1., 2., 4.]

    seq1_expected = compute_fft_magnitude(seq1_mapped)
    seq2_expected = compute_fft_magnitude(seq2_mapped)
    seq3_expected = compute_fft_magnitude(seq3_mapped)

    def assert_allclose(actual, expected, rtol=1e-5):
        assert len(actual) == len(expected), f"Length mismatch: {len(actual)} != {len(expected)}"
        for i, (a, e) in enumerate(zip(actual, expected)):
            diff = abs(a - e)
            assert diff <= rtol * max(abs(a), abs(e)) + 1e-8, f"Value mismatch at index {i}: {a} != {e}"

    assert_allclose(data["seq1"]["values"], seq1_expected)
    assert_allclose(data["seq2"]["values"], seq2_expected)
    assert_allclose(data["seq3"]["values"], seq3_expected)