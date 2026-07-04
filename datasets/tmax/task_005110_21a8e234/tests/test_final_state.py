# test_final_state.py

import os
import json
import subprocess
import pytest

def test_virtual_environment_exists():
    """Verify that the virtual environment was created and contains python."""
    python_path = '/home/user/sim_env/bin/python'
    assert os.path.isfile(python_path), f"Virtual environment python executable not found at {python_path}"

def test_summary_json_structure_and_integral():
    """Verify the existence and structure of summary.json, and the integral value."""
    summary_path = '/home/user/results/summary.json'
    assert os.path.isfile(summary_path), f"Summary JSON file not found at {summary_path}"

    with open(summary_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("summary.json is not a valid JSON file.")

    expected_keys = {"integral_yield", "forward_primer", "reverse_primer", "forward_gc", "reverse_gc"}
    missing_keys = expected_keys - set(data.keys())
    assert not missing_keys, f"summary.json is missing keys: {missing_keys}"

    # The integral should be approximately 291.68
    integral = data['integral_yield']
    assert isinstance(integral, (int, float)), "integral_yield must be a number"
    assert abs(integral - 291.68) < 1.0, f"Expected integral_yield around 291.68, got {integral}"

def test_hdf5_and_primers_via_student_env():
    """
    Use the student's virtual environment to read the HDF5 files, 
    verifying the simulation output and computing the expected primers.
    """
    python_exec = '/home/user/sim_env/bin/python'
    assert os.path.isfile(python_exec), "Cannot test HDF5: Student's virtual environment python not found."

    script = """
import h5py
import json
import sys

out = {}

try:
    # Check simulation.h5
    with h5py.File('/home/user/results/simulation.h5', 'r') as f:
        out['time_len'] = len(f['time'])
        out['has_temperature'] = 'temperature' in f
        out['has_concentration'] = 'concentration' in f
        out['total_yield'] = float(f.attrs['total_yield'])

    # Read reference.h5
    with h5py.File('/home/user/data/reference.h5', 'r') as f:
        seq = f['sequence'][()].decode('utf-8')

    target = seq[300:500]
    out['fwd'] = target[:20]

    comp = {'A':'T', 'T':'A', 'C':'G', 'G':'C'}
    out['rev'] = ''.join(comp[b] for b in reversed(target[-20:]))

    print(json.dumps(out))
except Exception as e:
    print(str(e), file=sys.stderr)
    sys.exit(1)
"""

    proc = subprocess.run([python_exec, '-c', script], capture_output=True, text=True)
    assert proc.returncode == 0, f"Failed to read HDF5 files using student's env (are h5py/numpy installed?). Error: {proc.stderr}"

    out = json.loads(proc.stdout)

    # Verify simulation.h5
    assert out['time_len'] == 500, f"Expected 500 time points in simulation.h5, got {out['time_len']}"
    assert out['has_temperature'], "Missing 'temperature' dataset in simulation.h5"
    assert out['has_concentration'], "Missing 'concentration' dataset in simulation.h5"
    assert abs(out['total_yield'] - 291.68) < 1.0, f"total_yield attribute in simulation.h5 is incorrect, got {out['total_yield']}"

    # Verify primer design in summary.json
    summary_path = '/home/user/results/summary.json'
    with open(summary_path, 'r') as f:
        data = json.load(f)

    assert data['forward_primer'] == out['fwd'], f"Forward primer mismatch. Expected {out['fwd']}, got {data['forward_primer']}"
    assert data['reverse_primer'] == out['rev'], f"Reverse primer mismatch. Expected {out['rev']}, got {data['reverse_primer']}"

    def calc_gc(s):
        if not s: return 0.0
        return sum(1 for b in s if b in 'GC') / len(s) * 100.0

    expected_fwd_gc = calc_gc(out['fwd'])
    expected_rev_gc = calc_gc(out['rev'])

    assert abs(data['forward_gc'] - expected_fwd_gc) < 0.1, f"Forward GC mismatch. Expected {expected_fwd_gc}, got {data['forward_gc']}"
    assert abs(data['reverse_gc'] - expected_rev_gc) < 0.1, f"Reverse GC mismatch. Expected {expected_rev_gc}, got {data['reverse_gc']}"